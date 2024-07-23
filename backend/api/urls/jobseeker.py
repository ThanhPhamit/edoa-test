from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from api.views import (
    JobseekerProposalViewSet,
    JobseekerJobseekerViewSet,
    JobseekerRecordViewSet,
    JobseekerJobseekerHistoryNotificationViewSet,
    JobseekerOrganizationCompanyViewSet,
    health_check,
)

router = routers.DefaultRouter()
router.register("proposals", JobseekerProposalViewSet)
router.register("jobseeker", JobseekerJobseekerViewSet)
router.register("records", JobseekerRecordViewSet)
router.register(
    "jobseeker_history_notifications", JobseekerJobseekerHistoryNotificationViewSet
)
router.register("organization_companies", JobseekerOrganizationCompanyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("health-check", health_check),
]
