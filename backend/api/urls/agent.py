from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from api.views import (
    UserViewSet,
    CompanyViewSet,
    JobCategoryViewSet,
    OrganizationJobCategoryViewSet,
    OrganizationCompanyViewSet,
    OrganizationCompanyAllViewSet,
    TagViewSet,
    JobseekerViewSet,
    JobseekerAllViewSet,
    JobViewSet,
    ProposalViewSet,
    ProposalBulkCreateView,
    ProposalBulkUpdateView,
    RecordViewSet,
    RecordNotificationAllViewSet,
    RecordBulkUpdateView,
    ManageUserView,
    JobLoadingViewSet,
    health_check,
)

app_name = "agent_recmii"

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("companies", CompanyViewSet)
router.register("job_categories", JobCategoryViewSet)
router.register("organization_job_categories", OrganizationJobCategoryViewSet)
router.register("organization_companies", OrganizationCompanyViewSet)
router.register("organization_companies_all", OrganizationCompanyAllViewSet)
router.register("tags", TagViewSet)
router.register("jobseekers", JobseekerViewSet)
router.register("jobseekers_all", JobseekerAllViewSet)
router.register("jobs", JobViewSet)
router.register("proposals", ProposalViewSet)
router.register("records", RecordViewSet)
router.register("record_notifications_all", RecordNotificationAllViewSet)
router.register("job_loadings", JobLoadingViewSet)

urlpatterns = [
    path("user/", ManageUserView.as_view(), name="user"),
    path("proposals/bulk_create/", ProposalBulkCreateView.as_view()),
    path("proposals/bulk_update/", ProposalBulkUpdateView.as_view()),
    path("records/bulk_update/", RecordBulkUpdateView.as_view()),
    path("", include(router.urls)),
    path("health-check", health_check),
]
