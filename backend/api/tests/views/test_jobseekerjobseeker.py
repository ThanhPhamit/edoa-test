from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

import datetime
from api.tests import factories
from api.views import JobseekerJobseekerViewSet


class JobseekerJobseekerTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.jobseeker_1 = factories.JobseekerFactory(
            organization_id=self.user.organization_id,
        )
        self.jobseeker_2 = factories.JobseekerFactory(
            organization_id=self.user.organization_id,
        )
        self.jobseeker_3 = factories.JobseekerFactory()

    def test_get_jobseekers(self):
        url = f"api/jobseeker/v1/jobseeker/"
        request = self.factory.get(url)
        view = JobseekerJobseekerViewSet.as_view({"get": "list"})

        """
        異常系 1:
        getできないこと
        """
        with self.assertRaises(AttributeError) as raises:
            view(request)

    def test_get_jobseeker(self):
        url = f"api/jobseeker/v1/jobseekers/{self.jobseeker_1.id}/"
        request = self.factory.get(url)
        view = JobseekerJobseekerViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.jobseeker_1.id)
        data = response.data

        """
        正常系 1:
        正常にデータをgetできること
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(data["id"], str(self.jobseeker_1.id), "id カラムの検証.")
        self.assertEqual(data["name"], self.jobseeker_1.name, "name カラムの検証.")
        self.assertEqual(
            data["in_charge_id"]["id"],
            self.jobseeker_1.in_charge_id.id,
            "in_charge_id id カラムの検証.",
        )
        self.assertEqual(
            data["last_record_at"],
            self.jobseeker_1.last_record_at.astimezone(
                datetime.timezone(datetime.timedelta(hours=9))
            ).isoformat(),
            "last_record_at カラムの検証.",
        )
        """
        異常系 1:
        項目を読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data["birth_date"]
        with self.assertRaises(KeyError) as raises:
            data["gender"]
        with self.assertRaises(KeyError) as raises:
            data["phone_number"]
        with self.assertRaises(KeyError) as raises:
            data["in_charge_id"]["password"]

    def test_post_jobseekers(self):
        url = f"api/jobseeker/v1/proposals/"
        data = {
            "name": "tanaka",
            "birth_date": "2023-05-01",
            "gender": "male",
            "phone_number": "00012345678",
            "in_charge_id": {"id": self.user.id},
            "last_record_at": "2023-06-01T13:49:37+09:00",
        }
        request = self.factory.post(
            url,
            data=data,
            format="json",
        )

        view = JobseekerJobseekerViewSet.as_view({"post": "create"})
        """
        異常系 1:
        postできないこと
        """
        with self.assertRaises(AttributeError) as raises:
            view(request)

    def test_put_jobseekers(self):
        url = f"api/jobseeker/v1/jobseekers/{self.jobseeker_1.id}/"
        data = {
            "id": self.jobseeker_1.id,
            "last_record_at": "2023-06-02T13:49:37+09:00",
        }
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )

        view = JobseekerJobseekerViewSet.as_view({"put": "update"})
        response = view(request, pk=self.jobseeker_1.id)
        data_id = response.data["id"]

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/jobseeker/v1/jobseekers/{self.jobseeker_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        view_get = JobseekerJobseekerViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.jobseeker_1.id)
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            str(data_id),
            "id カラムの検証.",
        )
        self.assertEqual(
            updated_data["last_record_at"],
            data["last_record_at"],
            "last_record_at カラムの検証.",
        )

    def test_delete_jobseeker(self):
        """
        正常系 1:
        正常にデータをdeleteできること
        """
        url = f"api/jobseeker/v1/jobseekers/{self.jobseeker_1.id}/"
        request = self.factory.delete(url)
        view = JobseekerJobseekerViewSet.as_view({"delete": "destroy"})

        """
        異常系 1:
        deleteできないこと
        """
        with self.assertRaises(AttributeError) as raises:
            view(request, pk=self.jobseeker_1.id)
