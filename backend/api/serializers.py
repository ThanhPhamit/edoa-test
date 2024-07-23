from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from rest_framework import serializers

from .models import (
    Organization,
    User,
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


class BulkSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        # FUTURE: Should be used to improve performance
        """
        try:
            self.child.Meta.model.objects.bulk_create(result, batch_size=100)
        except IntegrityError as e:
            raise ValidationError(e)
        """

        return result

    def update(self, instances, validated_data):
        result = [
            self.child.update(instance, attrs)
            for instance, attrs in zip(instances, validated_data)
        ]
        for instance in result:
            instance.updated_at = timezone.now()

        writable_fields = [
            x for x in self.child.Meta.fields if x not in ["id", "created_at"]
        ]

        try:
            self.child.Meta.model.objects.bulk_update(
                result, writable_fields, batch_size=100
            )
        except IntegrityError as e:
            raise ValidationError(e)

        return result


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    date_joined = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "name",
            "organization",
            "date_joined",
        ]
        read_only_fields = [
            "username",
        ]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

        def create(self, validated_data):
            user = get_user_model().objects.create_user(**validated_data)
            return user


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "corporate_number",
            "name",
            "company_url",
            "recruiting_url",
            "logo",
            "establishment_date",
            "is_listed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "corporate_number",
            "name",
            "company_url",
            "recruiting_url",
            "logo",
            "establishment_date",
            "is_listed",
        ]


class JobCategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = JobCategory
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "name",
        ]


class TagSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        instance = Tag.objects.create(
            name=validated_data["name"],
            organization=Organization.objects.get(
                id=self.context["request"].user.organization.id
            ),
        )
        instance.save()

        return instance


class OrganizationCompanySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    company = CompanySerializer(many=False, required=False, allow_null=True)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = OrganizationCompany
        fields = [
            "id",
            "name",
            "company_url",
            "summary",
            "total_employees",
            "profit",
            "service_years",
            "industry",
            "salary",
            "age",
            "female_rate",
            "disabled_rate",
            "monthly_overtime_hours",
            "acquisition_rate",
            "childcare_leave_rate",
            "other",
            "company",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        instance = OrganizationCompany.objects.create(
            name=validated_data["name"],
            company_url=validated_data["company_url"],
            summary=validated_data["summary"],
            total_employees=validated_data["total_employees"],
            profit=validated_data["profit"],
            service_years=validated_data["service_years"],
            industry=validated_data["industry"],
            salary=validated_data["salary"],
            age=validated_data["age"],
            female_rate=validated_data["female_rate"],
            disabled_rate=validated_data["disabled_rate"],
            monthly_overtime_hours=validated_data["monthly_overtime_hours"],
            acquisition_rate=validated_data["acquisition_rate"],
            childcare_leave_rate=validated_data["childcare_leave_rate"],
            other=validated_data["other"],
            company=Company.objects.get(id=validated_data["company"]["id"])
            if validated_data["company"] != None
            else None,
            organization=Organization.objects.get(
                id=self.context["request"].user.organization.id
            ),
        )
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.summary = validated_data["summary"]
        instance.total_employees = validated_data["total_employees"]
        instance.profit = validated_data["profit"]
        instance.service_years = validated_data["service_years"]
        instance.industry = validated_data["industry"]
        instance.salary = validated_data["salary"]
        instance.age = validated_data["age"]
        instance.female_rate = validated_data["female_rate"]
        instance.disabled_rate = validated_data["disabled_rate"]
        instance.monthly_overtime_hours = validated_data["monthly_overtime_hours"]
        instance.acquisition_rate = validated_data["acquisition_rate"]
        instance.childcare_leave_rate = validated_data["childcare_leave_rate"]
        instance.other = validated_data["other"]
        instance.company = Company.objects.get(id=validated_data["company"]["id"]) if validated_data["company"] != None else None
        instance.save()

        return instance


class OrganizationCompanyAllSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True, required=False)

    class Meta:
        model = OrganizationCompany
        fields = [
            "id",
            "name",
            "company_url",
            "company",
        ]


class JobseekerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    in_charge = UserSerializer(many=False, allow_null=True)
    # proposals = ProposalSerializer(source="proposal_set", many=True)

    class Meta:
        model = Jobseeker
        fields = [
            "id",
            "name",
            "birth_date",
            "gender",
            "phone_number",
            "email",
            "in_charge",
            "last_record_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        instance = Jobseeker.objects.create(
            name=validated_data["name"],
            birth_date=validated_data["birth_date"],
            gender=validated_data["gender"],
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            in_charge=User.objects.get(id=validated_data["in_charge"]["id"])
            if validated_data["in_charge"] != None
            else None,
            last_record_at=validated_data["last_record_at"],
            organization=Organization.objects.get(
                id=self.context["request"].user.organization.id
            ),
        )
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.birth_date = validated_data["birth_date"]
        instance.gender = validated_data["gender"]
        instance.phone_number = validated_data["phone_number"]
        instance.email = validated_data["email"]
        instance.in_charge = (
            User.objects.get(id=validated_data["in_charge"]["id"])
            if validated_data["in_charge"] != None
            else None
        )
        instance.last_record_at = validated_data["last_record_at"]
        instance.save()

        return instance


class JobSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    organization_company = OrganizationCompanySerializer(many=False)
    job_category = JobCategorySerializer(many=False)

    class Meta:
        model = Job
        fields = [
            "id",
            "organization_company",
            "job_category",
            "position",
            "layer",
            "min_salary",
            "max_salary",
            "salary",
            "employment_status",
            "summary",
            "min_qualifications",
            "pfd_qualifications",
            "ideal_profile",
            "address",
            "remote",
            "working_hours",
            "holiday",
            "benefit",
            "trial_period",
            "smoking_prevention_measure",
            "other",
            "source_url",
            "is_archive",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        instance = Job.objects.create(
            organization_company=OrganizationCompany.objects.get(
                id=validated_data["organization_company"]["id"]
            ),
            job_category=JobCategory.objects.get(
                id=validated_data["job_category"]["id"]
            ),
            position=validated_data["position"],
            layer=validated_data["layer"],
            min_salary=validated_data["min_salary"],
            max_salary=validated_data["max_salary"],
            salary=validated_data["salary"],
            employment_status=validated_data["employment_status"],
            summary=validated_data["summary"],
            min_qualifications=validated_data["min_qualifications"],
            pfd_qualifications=validated_data["pfd_qualifications"],
            ideal_profile=validated_data["ideal_profile"],
            address=validated_data["address"],
            remote=validated_data["remote"],
            working_hours=validated_data["working_hours"],
            holiday=validated_data["holiday"],
            benefit=validated_data["benefit"],
            trial_period=validated_data["trial_period"],
            smoking_prevention_measure=validated_data["smoking_prevention_measure"],
            source_url=validated_data["source_url"],
            other=validated_data["other"],
            is_archive=validated_data["is_archive"],
            organization=Organization.objects.get(
                id=self.context["request"].user.organization.id
            ),
        )
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.organization_company = OrganizationCompany.objects.get(
            id=validated_data["organization_company"]["id"]
        )
        instance.job_category = JobCategory.objects.get(
            id=validated_data["job_category"]["id"]
        )
        instance.position = validated_data["position"]
        instance.layer = validated_data["layer"]
        instance.min_salary = validated_data["min_salary"]
        instance.max_salary = validated_data["max_salary"]
        instance.salary = validated_data["salary"]
        instance.employment_status = validated_data["employment_status"]
        instance.summary = validated_data["summary"]
        instance.min_qualifications = validated_data["min_qualifications"]
        instance.pfd_qualifications = validated_data["pfd_qualifications"]
        instance.ideal_profile = validated_data["ideal_profile"]
        instance.address = validated_data["address"]
        instance.remote = validated_data["remote"]
        instance.working_hours = validated_data["working_hours"]
        instance.holiday = validated_data["holiday"]
        instance.benefit = validated_data["benefit"]
        instance.trial_period = validated_data["trial_period"]
        instance.smoking_prevention_measure = validated_data[
            "smoking_prevention_measure"
        ]
        instance.other = validated_data["other"]
        instance.source_url = validated_data["source_url"]
        instance.is_archive = validated_data["is_archive"]
        instance.save()

        return instance


class ProposalSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    jobseeker = JobseekerSerializer(many=False)
    job = JobSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Proposal
        fields = [
            "id",
            "jobseeker",
            "job",
            "intention",
            "is_favorite",
            "comment",
            "is_public",
            "is_checked",
            "position",
            "salary",
            "employment_status",
            "summary",
            "min_qualifications",
            "pfd_qualifications",
            "ideal_profile",
            "address",
            "working_hours",
            "holiday",
            "benefit",
            "trial_period",
            "smoking_prevention_measure",
            "other",
            "tags",
            "is_appeal_layer",
            "is_appeal_remote",
            "published_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "jobseeker",
            "job",
        ]
        list_serializer_class = BulkSerializer

    def create(self, validated_data):
        latest_proposal = Proposal.objects.filter(
            job__id__exact=validated_data["job"]["id"]
        ).order_by("-created_at")[:1]
        if latest_proposal.count() > 0:
            tagsObj = latest_proposal[0].tags.all()
        else:
            tagsObj = Tag.objects.none()

        instance = Proposal(
            jobseeker=Jobseeker.objects.get(id=validated_data["jobseeker"]["id"]),
            job=Job.objects.get(id=validated_data["job"]["id"]),
            intention=validated_data["intention"],
            is_favorite=validated_data["is_favorite"],
            comment=validated_data["comment"],
            is_public=validated_data["is_public"],
            is_checked=validated_data["is_checked"],
            position=validated_data["position"],
            salary=validated_data["salary"],
            employment_status=validated_data["employment_status"],
            summary=validated_data["summary"],
            min_qualifications=validated_data["min_qualifications"],
            pfd_qualifications=validated_data["pfd_qualifications"],
            ideal_profile=validated_data["ideal_profile"],
            address=validated_data["address"],
            working_hours=validated_data["working_hours"],
            holiday=validated_data["holiday"],
            benefit=validated_data["benefit"],
            trial_period=validated_data["trial_period"],
            smoking_prevention_measure=validated_data["smoking_prevention_measure"],
            other=validated_data["other"],
            is_appeal_layer=validated_data["is_appeal_layer"],
            is_appeal_remote=validated_data["is_appeal_remote"],
            published_at=validated_data["published_at"],
            organization=Organization.objects.get(
                id=self.context["request"].user.organization.id
            ),
        )

        instance.save()

        if len(validated_data["tags"]) > 0:
            for tag in validated_data["tags"]:
                tagObj = Tag.objects.get(id=tag["id"])
                instance.tags.add(
                    tagObj,
                    through_defaults={
                        "organization_id": self.context["request"].user.organization.id
                    },
                )
        else:
            for tagObj in tagsObj:
                instance.tags.add(
                    tagObj,
                    through_defaults={
                        "organization_id": self.context["request"].user.organization.id
                    },
                )
        return instance

    def update(self, instance, validated_data):
        instance.intention = validated_data.get("intention", instance.intention)
        instance.is_favorite = validated_data.get("is_favorite", instance.is_favorite)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.is_public = validated_data.get("is_public", instance.is_public)
        instance.is_checked = validated_data.get("is_checked", instance.is_checked)
        instance.position = validated_data.get("position", instance.position)
        instance.salary = validated_data.get("salary", instance.salary)
        instance.employment_status = validated_data.get(
            "employment_status", instance.employment_status
        )
        instance.summary = validated_data.get("summary", instance.summary)
        instance.min_qualifications = validated_data.get(
            "min_qualifications", instance.min_qualifications
        )
        instance.pfd_qualifications = validated_data.get(
            "pfd_qualifications", instance.pfd_qualifications
        )
        instance.ideal_profile = validated_data.get(
            "ideal_profile", instance.ideal_profile
        )
        instance.address = validated_data.get("address", instance.address)
        instance.working_hours = validated_data.get(
            "working_hours", instance.working_hours
        )
        instance.holiday = validated_data.get("holiday", instance.holiday)
        instance.benefit = validated_data.get("benefit", instance.benefit)
        instance.trial_period = validated_data.get(
            "trial_period", instance.trial_period
        )
        instance.smoking_prevention_measure = validated_data.get(
            "smoking_prevention_measure", instance.smoking_prevention_measure
        )
        instance.other = validated_data.get("other", instance.other)
        instance.is_appeal_layer = validated_data.get(
            "is_appeal_layer", instance.is_appeal_layer
        )
        instance.is_appeal_remote = validated_data.get(
            "is_appeal_remote", instance.is_appeal_remote
        )
        instance.published_at = validated_data.get(
            "published_at", instance.published_at
        )

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        proposal = Proposal.objects.get(id=instance.id)
        proposal.tags.clear()

        for tag in validated_data.get("tags", instance.tags.all()):
            tagObj = Tag.objects.get(id=tag["id"])
            instance.tags.add(
                tagObj,
                through_defaults={
                    "organization_id": self.context["request"].user.organization.id
                },
            )

        return instance


class RecordSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    proposal = ProposalSerializer(many=False)

    class Meta:
        model = Record
        fields = [
            "id",
            "proposal",
            "before_record_at",
            "is_long_time",
            "is_checked",
            "trigger",
            "created_at",
            "updated_at",
        ]
        list_serializer_class = BulkSerializer

    def create(self, validated_data):
        instance = Record.objects.create(
            proposal=Proposal.objects.get(id=validated_data["proposal"]["id"]),
            before_record_at=validated_data["before_record_at"],
            is_long_time=validated_data["is_long_time"],
            is_checked=validated_data["is_checked"],
            organization=Organization.objects.get(
                id=self.context["request"].user.organization.id
            ),
        )
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.proposal = Proposal.objects.get(id=validated_data["proposal"]["id"])
        instance.before_record_at = validated_data["before_record_at"]
        instance.is_long_time = validated_data["is_long_time"]
        instance.is_checked = validated_data["is_checked"]
        instance.trigger = validated_data["trigger"]

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance


class JobseekerProposalSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    job = JobSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Proposal
        fields = [
            "id",
            "job",
            "intention",
            "is_favorite",
            "comment",
            "is_public",
            "is_checked",
            "position",
            "salary",
            "employment_status",
            "summary",
            "min_qualifications",
            "pfd_qualifications",
            "ideal_profile",
            "address",
            "working_hours",
            "holiday",
            "benefit",
            "trial_period",
            "smoking_prevention_measure",
            "other",
            "tags",
            "is_appeal_layer",
            "is_appeal_remote",
            "published_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "job",
            "comment",
            "is_public",
            "position",
            "salary",
            "employment_status",
            "summary",
            "min_qualifications",
            "pfd_qualifications",
            "ideal_profile",
            "address",
            "working_hours",
            "holiday",
            "benefit",
            "trial_period",
            "smoking_prevention_measure",
            "other",
            "tags",
            "is_appeal_layer",
            "is_appeal_remote",
            "published_at",
        ]

    def update(self, instance, validated_data):
        instance.intention = validated_data["intention"]
        instance.is_favorite = validated_data["is_favorite"]
        instance.is_checked = validated_data["is_checked"]
        instance.save()

        return instance


class JobseekerJobseekerSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(required=True)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    in_charge = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Jobseeker
        fields = [
            "id",
            "name",
            "in_charge",
            "last_record_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "name",
            "in_charge",
        ]


class JobseekerRecordSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    proposal = JobseekerProposalSerializer(many=False)

    class Meta:
        model = Record
        fields = [
            "id",
            "proposal",
            "before_record_at",
            "is_long_time",
            "is_checked",
            "trigger",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        instance = Record.objects.create(
            proposal=Proposal.objects.get(id=validated_data["proposal"]["id"]),
            before_record_at=validated_data["before_record_at"],
            is_long_time=validated_data["is_long_time"],
            is_checked=validated_data["is_checked"],
            trigger=validated_data["trigger"],
            organization=Organization.objects.get(
                id=Proposal.objects.get(
                    id=validated_data["proposal"]["id"]
                ).organization.id
            ),
        )
        instance.save()

        return instance


class JobseekerJobseekerHistoryNotificationSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    record = JobseekerRecordSerializer(many=False)

    class Meta:
        model = JobseekerHistoryNotification
        fields = [
            "id",
            "record",
            "is_send",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        instance = JobseekerHistoryNotification.objects.create(
            record=Record.objects.get(id=validated_data["record"]["id"]),
            is_send=validated_data["is_send"],
            organization=Organization.objects.get(
                id=Record.objects.get(id=validated_data["record"]["id"]).organization.id
            ),
        )
        instance.save()

        return instance


class JobseekerOrganizationCompanySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = OrganizationCompany
        fields = [
            "id",
            "name",
            "summary",
            "total_employees",
            "profit",
            "service_years",
            "industry",
            "salary",
            "age",
            "female_rate",
            "disabled_rate",
            "monthly_overtime_hours",
            "acquisition_rate",
            "childcare_leave_rate",
            "other",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "name",
            "summary",
            "total_employees",
            "profit",
            "service_years",
            "industry",
            "salary",
            "age",
            "female_rate",
            "disabled_rate",
            "monthly_overtime_hours",
            "acquisition_rate",
            "childcare_leave_rate",
            "other",
        ]


class JobLoadingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = JobLoading
        fields = [
            "id",
            "source_url",
            "is_completed",
            "is_error",
            "error_message",
            "position",
            "salary",
            "employment_status",
            "summary",
            "min_qualifications",
            "pfd_qualifications",
            "ideal_profile",
            "address",
            "benefit",
            "other",
            "company_name",
            "job_category_name",
            "holiday",
            "working_hours",
            "smoking_prevention_measure",
            "trial_period",
            "layer",
            "remote",
            "min_salary",
            "max_salary",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        instance = JobLoading.objects.create(
            organization=Organization.objects.get(
                id=self.context["request"].user.organization.id
            ),
            user=User.objects.get(id=self.context["request"].user.id),
            source_url=validated_data["source_url"],
        )
        instance.save()
        return instance
