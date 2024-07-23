from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories
from api.views import JobseekerViewSet
import datetime


class JobseekerTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.jobseeker_1 = factories.JobseekerFactory(
            organization_id=self.user.organization_id
        )
        self.jobseeker_2 = factories.JobseekerFactory(
            organization_id=self.user.organization_id
        )
        self.jobseeker_3 = factories.JobseekerFactory()

    def test_get_jobseekers(self):
        url = f"api/agent/v1/jobseekers/"
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobseekerViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data["results"]), 2, "2件取得できること.")
        self.assertEqual(data["count"], 2, "2件取得できること.")

        self.assertEqual(
            data["results"][0]["id"], str(self.jobseeker_2.id), "id カラムの検証."
        )
        self.assertEqual(
            data["results"][0]["name"], self.jobseeker_2.name, "name カラムの検証."
        )
        self.assertEqual(
            data["results"][0]["birth_date"],
            self.jobseeker_2.birth_date,
            "birth_date カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["gender"], self.jobseeker_2.gender, "gender カラムの検証."
        )
        self.assertEqual(
            data["results"][0]["phone_number"],
            self.jobseeker_2.phone_number,
            "phone_number カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["in_charge_id"]["id"],
            self.jobseeker_2.in_charge_id.id,
            "in_charge_id id カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["last_record_at"],
            self.jobseeker_2.last_record_at.astimezone(
                datetime.timezone(datetime.timedelta(hours=9))
            ).isoformat(),
            "last_record_at カラムの検証.",
        )

        """
        異常系 1:
        パスワードを読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data["results"][0]["in_charge_id"]["password"]

        """
        異常系 2:
        認証されていないユーザーがgetをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.get(url)
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(
            reponse_unauthorize.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "HTTPステータス401が返ること.",
        )

    def test_search_jobseekers_name(self):
        keyword = self.jobseeker_1.name[0:5]
        url = "".join([reverse("agent_recmii:jobseeker-list")]) + f"?keyword={keyword}"

        """
        正常系 1:
        jobseekerのnameで前方一致検索され正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobseekerViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data["results"]), 1, "1件取得できること.")
        self.assertEqual(data["count"], 1, "1件取得できること.")
        self.assertEqual(
            data["results"][0]["id"], str(self.jobseeker_1.id), "id カラムの検証."
        )

    def test_search_jobseekers_phonenumber(self):
        keyword = self.jobseeker_1.phone_number[0:5]
        url = "".join([reverse("agent_recmii:jobseeker-list")]) + f"?keyword={keyword}"

        """
        正常系 1:
        jobseekerのphone_numberで前方一致検索され正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobseekerViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data["results"]), 1, "1件取得できること.")
        self.assertEqual(data["count"], 1, "1件取得できること.")
        self.assertEqual(
            data["results"][0]["id"], str(self.jobseeker_1.id), "id カラムの検証."
        )

    def test_get_jobseeker(self):
        url = f"api/agent/v1/jobseekers/{self.jobseeker_1.id}/"

        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobseekerViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.jobseeker_1.id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(data["id"], str(self.jobseeker_1.id), "id カラムの検証.")
        self.assertEqual(data["name"], self.jobseeker_1.name, "name カラムの検証.")
        self.assertEqual(
            data["birth_date"],
            self.jobseeker_1.birth_date,
            "birth_date カラムの検証.",
        )
        self.assertEqual(data["gender"], self.jobseeker_1.gender, "gender カラムの検証.")
        self.assertEqual(
            data["phone_number"], self.jobseeker_1.phone_number, "phone_number カラムの検証."
        )
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
        パスワードを読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data["in_charge_id"]["password"]

        """
        異常系 2:
        認証されていないユーザーがgetをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.get(url)
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(
            reponse_unauthorize.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "HTTPステータス401が返ること.",
        )

    def test_post_jobseekers(self):
        url = "".join([reverse("agent_recmii:jobseeker-list")])
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
        force_authenticate(request, user=self.user)
        view = JobseekerViewSet.as_view({"post": "create"})
        response = view(request)
        data_id = response.data["id"]

        """
        正常系 1:
        正常にデータをpostできること
        """
        url_updated_data = f"api/agent/v1/jobseekers/{data_id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = JobseekerViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=data_id)
        updated_data = response_updated_data.data

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, "HTTPステータス201が返ること."
        )
        self.assertEqual(
            updated_data["id"],
            str(data_id),
            "id カラムの検証.",
        )
        self.assertEqual(updated_data["name"], data["name"], "name カラムの検証.")
        self.assertEqual(
            updated_data["birth_date"],
            data["birth_date"],
            "birth_date カラムの検証.",
        )
        self.assertEqual(updated_data["gender"], data["gender"], "gender カラムの検証.")
        self.assertEqual(
            updated_data["phone_number"],
            data["phone_number"],
            "phone_number カラムの検証.",
        )
        self.assertEqual(
            updated_data["in_charge_id"]["id"],
            data["in_charge_id"]["id"],
            "in_charge_id id カラムの検証.",
        )
        self.assertEqual(
            updated_data["last_record_at"],
            data["last_record_at"],
            "last_record_at カラムの検証.",
        )

        """
        異常系 1:
        認証されていないユーザーがpostをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.get(url)
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(
            reponse_unauthorize.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "HTTPステータス401が返ること.",
        )

    def test_put_jobseekers(self):
        url = f"api/agent/v1/jobseekers/{self.jobseeker_1.id}/"
        data = {
            "id": self.jobseeker_1.id,
            "name": "yamamoto",
            "birth_date": "2023-05-02",
            "gender": "female",
            "phone_number": "11112345678",
            "in_charge_id": {"id": self.user.id},
            "last_record_at": "2023-06-02T13:49:37+09:00",
        }
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )

        force_authenticate(request, user=self.user)
        view = JobseekerViewSet.as_view({"put": "update"})
        response = view(request, pk=self.jobseeker_1.id)
        data_id = response.data["id"]

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/jobseekers/{self.jobseeker_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = JobseekerViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.jobseeker_1.id)
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            str(data_id),
            "id カラムの検証.",
        )
        self.assertEqual(updated_data["name"], data["name"], "name カラムの検証.")
        self.assertEqual(
            updated_data["birth_date"],
            data["birth_date"],
            "birth_date カラムの検証.",
        )
        self.assertEqual(updated_data["gender"], data["gender"], "gender カラムの検証.")
        self.assertEqual(
            updated_data["phone_number"],
            data["phone_number"],
            "phone_number カラムの検証.",
        )
        self.assertEqual(
            updated_data["in_charge_id"]["id"],
            data["in_charge_id"]["id"],
            "in_charge_id id カラムの検証.",
        )
        self.assertEqual(
            updated_data["last_record_at"],
            data["last_record_at"],
            "last_record_at カラムの検証.",
        )

        """
        異常系 1:
        認証されていないユーザーがputをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.get(url)
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(
            reponse_unauthorize.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "HTTPステータス401が返ること.",
        )

    def test_delete_jobseeker(self):
        """
        正常系 1:
        正常にデータをdeleteできること
        """
        url = f"api/agent/v1/jobseekers/{self.jobseeker_1.id}/"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = JobseekerViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.jobseeker_1.id)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, "HTTPステータス204が返ること."
        )

        """
        異常系 1:
        削除されたデータにgetをリクエストした場合、エラーが返ること
        """
        url_updated_data = f"api/agent/v1/jobseekers/{self.jobseeker_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = JobseekerViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.jobseeker_1.id)

        self.assertEqual(
            response_updated_data.status_code,
            status.HTTP_404_NOT_FOUND,
            "HTTPステータス404が返ること.",
        )
        """
        異常系 2:
        認証されていないユーザーがdeleteをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.get(url)
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(
            reponse_unauthorize.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "HTTPステータス401が返ること.",
        )
