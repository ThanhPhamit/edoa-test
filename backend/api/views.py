from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q, OuterRef, Subquery, Count

from functools import wraps
import jwt

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from django.db import transaction

from .models import (
    Company,
    JobCategory,
    OrganizationCompany,
    Tag,
    Jobseeker,
    Job,
    Proposal,
    Record,
    JobseekerHistoryNotification,
    JobLoading,
)
from .serializers import (
    UserSerializer,
    CompanySerializer,
    JobCategorySerializer,
    OrganizationCompanySerializer,
    OrganizationCompanyAllSerializer,
    TagSerializer,
    JobseekerSerializer,
    JobSerializer,
    ProposalSerializer,
    RecordSerializer,
    JobseekerJobseekerHistoryNotificationSerializer,
    JobseekerProposalSerializer,
    JobseekerJobseekerSerializer,
    JobseekerRecordSerializer,
    JobseekerOrganizationCompanySerializer,
    JobLoadingSerializer,
)
from .pagination import StandardResultsSetPagination
from .tasks import (
    exec_mail_agent_longtime,
    exec_mail_jobseeker_proposal,
    exec_mail_ops_add_company,
    exec_job_loading,
)


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header"""
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """

    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, options={"verify_signature": False})
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse(
                {"message": "You don't have access to this resource"}
            )
            response.status_code = 403
            return response

        return decorated

    return require_scope


def health_check(request):
    return JsonResponse({"status": "healthy"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = (
        get_user_model()
        .objects.select_related("organization")
        .order_by("date_joined")
        .reverse()
        .all()
    )
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        return queryset


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.order_by("name").all()
    serializer_class = CompanySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.queryset
        q = self.request.query_params.get("q", "").strip()
        if q:
            # NOTE: django's filter(name__icontains=q) will create the query using UPPER functions, which won't use postgresql's trgm index.
            #       instead, use ILIKE here for using trgm index.
            queryset = queryset.extra(where=["name ILIKE %s"], params=["%" + q + "%"])

        url = self.request.query_params.get("url", "").strip()
        if url:
            if url[-1] == "/":
                url_without_slash = url[:-1]
            else:
                url_without_slash = url
            url_with_slash = url_without_slash + "/"
            queryset = queryset.filter(
                Q(company_url__exact=url_without_slash)
                | Q(company_url__exact=url_with_slash)
            )

        top = self.request.query_params.get("top", None)
        if top:
            try:
                top_count = int(top)
                queryset = queryset[:top_count]
            except ValueError:
                return Response(
                    {"top": ["Invalid value for top."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"top": ["This field is required"]}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.order_by("name").all()
    serializer_class = JobCategorySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class OrganizationJobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.prefetch_related("job").order_by("name").all()
    serializer_class = JobCategorySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(
            job__organization=self.request.user.organization
        ).distinct()
        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class OrganizationCompanyViewSet(viewsets.ModelViewSet):
    queryset = (
        OrganizationCompany.objects.select_related("company", "organization")
        .order_by("company__name")
        .all()
    )
    serializer_class = OrganizationCompanySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        if self.request.query_params.get("company_id", None) is not None:
            queryset = queryset.filter(
                Q(company__id__exact=self.request.query_params.get("company_id", None))
            ).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if serializer.data["company"] is None:
            exec_mail_ops_add_company.delay(serializer.data["id"])

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class OrganizationCompanyAllViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        OrganizationCompany.objects.select_related("company", "organization")
        .order_by("company__name")
        .all()
    )
    serializer_class = OrganizationCompanyAllSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.select_related("organization").order_by("created_at").all()
    serializer_class = TagSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobseekerViewSet(viewsets.ModelViewSet):
    queryset = (
        Jobseeker.objects.select_related("in_charge", "organization")
        .prefetch_related("proposals")
        .order_by("created_at")
        .reverse()
        .all()
    )
    serializer_class = JobseekerSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        if self.request.query_params.get("keyword", None) is not None:
            queryset = queryset.filter(
                Q(name__istartswith=self.request.query_params.get("keyword", None))
                | Q(
                    phone_number__istartswith=self.request.query_params.get(
                        "keyword", None
                    )
                )
            ).distinct()

        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobseekerAllViewSet(viewsets.ModelViewSet):
    queryset = (
        Jobseeker.objects.select_related("in_charge", "organization")
        .prefetch_related("proposals")
        .all()
    )
    serializer_class = JobseekerSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        return queryset

    def list(self, request):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        q = self.request.query_params.get("q", "").strip()
        if q:
            # NOTE: django's filter(name__icontains=q) will create the query using UPPER functions, which won't use postgresql's trgm index.
            #       instead, use ILIKE here for using trgm index.
            queryset = queryset.filter(name__istartswith=q)

        top = self.request.query_params.get("top", None)
        if top:
            try:
                top_count = int(top)
                queryset = queryset[:top_count]
            except ValueError:
                return Response(
                    {"top": ["Invalid value for top."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"top": ["This field is required"]}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobViewSet(viewsets.ModelViewSet):
    queryset = (
        Job.objects.select_related(
            "organization_company",
            "job_category",
            "organization",
        )
        .prefetch_related("proposal_set")
        .order_by("created_at")
        .reverse()
        .all()
    )
    serializer_class = JobSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        if self.request.query_params.get("is_archive", None) == "true":
            queryset = queryset.filter(is_archive__exact=True)
        elif self.request.query_params.get("is_archive", None) == "false":
            queryset = queryset.filter(is_archive__exact=False)
        if self.request.query_params.get("keyword", None) is not None:
            queryset = queryset.filter(
                Q(
                    organization_company__name__icontains=self.request.query_params.get(
                        "keyword", None
                    )
                )
                | Q(position__icontains=self.request.query_params.get("keyword", None))
            ).distinct()
        if self.request.query_params.getlist("job_category[]", None) is not None:
            if len(self.request.query_params.getlist("job_category[]", None)) > 0:
                queryset = queryset.filter(
                    job_category__in=self.request.query_params.getlist(
                        "job_category[]", None
                    ),
                )
        if (
            self.request.query_params.get("min_salary", None) is not None
            and self.request.query_params.get("max_salary", None) is not None
        ):
            if int(self.request.query_params.get("min_salary", None)) <= int(
                self.request.query_params.get("max_salary", None)
            ):
                queryset = (
                    queryset.exclude(
                        (
                            Q(
                                min_salary__gte=self.request.query_params.get(
                                    "max_salary", None
                                )
                            )
                            & Q(min_salary__isnull=False)
                        )
                        | (
                            Q(
                                max_salary__lte=self.request.query_params.get(
                                    "min_salary", None
                                )
                            )
                            & Q(max_salary__isnull=False)
                        )
                    )
                    .filter(Q(max_salary__isnull=False) | Q(min_salary__isnull=False))
                    .distinct()
                )
            else:
                queryset = Job.objects.none()
        elif (
            self.request.query_params.get("min_salary", None) is None
            and self.request.query_params.get("max_salary", None) is not None
        ):
            queryset = (
                queryset.exclude(
                    (
                        Q(
                            min_salary__gte=self.request.query_params.get(
                                "max_salary", None
                            )
                        )
                        & Q(min_salary__isnull=False)
                    )
                )
                .filter(Q(max_salary__isnull=False) | Q(min_salary__isnull=False))
                .distinct()
            )
        elif (
            self.request.query_params.get("min_salary", None) is not None
            and self.request.query_params.get("max_salary", None) is None
        ):
            queryset = (
                queryset.exclude(
                    (
                        Q(
                            max_salary__lte=self.request.query_params.get(
                                "min_salary", None
                            )
                        )
                        & Q(max_salary__isnull=False)
                    )
                )
                .filter(Q(max_salary__isnull=False) | Q(min_salary__isnull=False))
                .distinct()
            )
        if self.request.query_params.get("layer", None) is not None:
            queryset = queryset.filter(
                layer__exact=self.request.query_params.get("layer", None),
            )
        if self.request.query_params.get("remote", None) is not None:
            queryset = queryset.filter(
                remote__exact=self.request.query_params.get("remote", None),
            )
        if self.request.query_params.getlist("tags[]", None):
            latest_proposal_subquery = (
                Proposal.objects.filter(job=OuterRef("pk"))
                .order_by("-created_at")
                .values("id")[:1]
            )
            queryset = (
                queryset.filter(proposal=Subquery(latest_proposal_subquery))
                .annotate(
                    matching_tags_count=Count(
                        "proposal__tags",
                        filter=Q(
                            proposal__tags__id__in=self.request.query_params.getlist(
                                "tags[]", None
                            )
                        ),
                    ),
                )
                .filter(
                    matching_tags_count=len(
                        self.request.query_params.getlist("tags[]", None)
                    ),
                )
            )

        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class ProposalViewSet(viewsets.ModelViewSet):
    queryset = (
        Proposal.objects.select_related(
            "jobseeker",
            "job",
            "organization",
        )
        .prefetch_related("tags")
        .order_by("created_at")
        .reverse()
        .all()
    )
    serializer_class = ProposalSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        if self.request.query_params.get("keyword", None) is not None:
            queryset = queryset.filter(
                Q(jobseeker__id__exact=self.request.query_params.get("keyword", None))
            )
        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class ProposalBulkCreateView(generics.CreateAPIView):
    serializer_class = ProposalSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)


# Note: the way using self.perform_update throws the error: "bulk_update() can only be used with concrete fields"
#       It looks due to the limitation of the UpdateAPIView's build_update, so just update proposals one by one.
# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class ProposalBulkUpdateView(generics.UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = ProposalSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def partial_update(self, request, *args, **kwargs):
        proposal_data_list = request.data["proposals"]
        updated_data = []
        with transaction.atomic():
            for proposal_data in proposal_data_list:
                proposal_id = proposal_data.get("id")
                if proposal_id is None:
                    transaction.set_rollback(True)
                    return Response(
                        {"detail": "Each proposal data must contain 'id' field."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    proposal = Proposal.objects.get(id=proposal_id)
                except Proposal.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response(
                        {"detail": f"Proposal with ID {proposal_id} not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                serializer = self.get_serializer(
                    proposal, data=proposal_data, partial=True
                )
                if not serializer.is_valid():
                    transaction.set_rollback(True)
                    return Response(
                        {"detail": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                serializer.save()
                updated_data.append(serializer.data)

            if request.data["is_email"]:
                exec_mail_jobseeker_proposal.delay(request.data["jobseeker_id"])

        return Response(updated_data, status=status.HTTP_200_OK)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class RecordViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Record.objects.select_related(
            "proposal",
            "organization",
        )
        .order_by("created_at")
        .reverse()
        .all()
    )
    serializer_class = RecordSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization)
        if self.request.query_params.get("keyword", None) is not None:
            queryset = queryset.filter(
                Q(
                    proposal__jobseeker__id__exact=self.request.query_params.get(
                        "keyword", None
                    )
                )
            ).distinct()
        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class RecordBulkUpdateView(generics.UpdateAPIView):
    serializer_class = RecordSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instances = Record.objects.filter(
            id__in=[x["id"] for x in request.data],
        )
        serializer = self.get_serializer(instances, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class RecordNotificationAllViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Record.objects.select_related(
        "proposal",
        "organization",
    ).all()
    serializer_class = RecordSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(
            organization=self.request.user.organization,
            proposal__jobseeker__in_charge=self.request.user.id,
            is_checked=False,
        )

        if self.request.query_params.get("keyword", None) is not None:
            queryset = queryset.filter(
                Q(
                    proposal__jobseeker__id__exact=self.request.query_params.get(
                        "keyword", None
                    )
                )
            ).distinct()

        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobseekerProposalViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Proposal.objects.select_related(
            "jobseeker",
            "job",
            "organization",
        )
        .order_by("published_at")
        .reverse()
        .all()
    )
    serializer_class = JobseekerProposalSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = self.queryset.filter(
            jobseeker__id__exact=self.request.query_params.get("jobseeker_id", None)
        )
        if self.request.query_params.get("id", None) is not None:
            queryset = queryset.filter(
                id__exact=self.request.query_params.get("id", None)
            )
        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobseekerJobseekerViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Jobseeker.objects.select_related("in_charge", "organization")
        .prefetch_related("proposals")
        .all()
    )
    serializer_class = JobseekerJobseekerSerializer
    permission_classes = (AllowAny,)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobseekerRecordViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Record.objects.select_related(
        "proposal",
        "organization",
    ).all()
    serializer_class = JobseekerRecordSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if serializer.data["is_long_time"]:
            exec_mail_agent_longtime.delay(serializer.data["id"])

        return Response(serializer.data)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobseekerJobseekerHistoryNotificationViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = JobseekerHistoryNotification.objects.select_related("record").all()
    serializer_class = JobseekerJobseekerHistoryNotificationSerializer
    permission_classes = (AllowAny,)


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobseekerOrganizationCompanyViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        OrganizationCompany.objects.select_related("company", "organization")
        .order_by("company__name")
        .all()
    )
    serializer_class = JobseekerOrganizationCompanySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get("company_id", None) is not None:
            queryset = queryset.filter(
                Q(company__id__exact=self.request.query_params.get("company_id", None))
            ).distinct()
        return queryset


# @method_decorator(requires_scope('read:current_user'), name='dispatch')
class JobLoadingViewSet(viewsets.ModelViewSet):
    queryset = JobLoading.objects.order_by("created_at").all()
    serializer_class = JobLoadingSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(organization=self.request.user.organization, is_deleted=False)
        return queryset

    """
    request.data = {
        "source_url": "https://example.com",
    }
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        exec_job_loading.delay(serializer.data["id"], request.data["source_url"])

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # soft delete
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
