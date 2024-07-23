from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories

from api.views import ManageUserView


class ManageuserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.organization = factories.OrganizationFactory()
        self.user_1 = factories.UserFactory(organization_id=self.organization)
        self.user_2 = factories.UserFactory()

    def test_get_users(self):
        url = f"api/agent/v1/user/"

        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user_1)
        view = ManageUserView.as_view()
        response = view(request, pk=self.user_1.id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["id"],
            self.user_1.id,
            "id カラムの検証.",
        )
        self.assertEqual(
            data["username"],
            self.user_1.username,
            "username カラムの検証.",
        )
        self.assertEqual(
            data["name"],
            self.user_1.name,
            "name カラムの検証.",
        )
        """
        異常系 1:
        パスワードを読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data["password"]

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

    def test_get_user(self):
        url = f"api/agent/v1/user/{self.user_1.id}/"

        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user_1)
        view = ManageUserView.as_view()
        response = view(request, pk=self.user_1.id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["id"],
            self.user_1.id,
            "id カラムの検証.",
        )
        self.assertEqual(
            data["username"],
            self.user_1.username,
            "username カラムの検証.",
        )
        self.assertEqual(
            data["name"],
            self.user_1.name,
            "name カラムの検証.",
        )
        """
        異常系 1:
        パスワードを読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data["password"]

        """
        異常系 1:
        認証されていないユーザーがgetをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.get(url)
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(
            reponse_unauthorize.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "HTTPステータス401が返ること.",
        )

    def test_post_user(self):
        url = f"api/agent/v1/user/"
        request = self.factory.post(
            url,
            data={
                "username": "kimoto",
                "name": "kimoto",
                "logo": None,
                "organization_id": self.organization.id,
            },
            format="json",
        )
        force_authenticate(request, user=self.user_1)
        view = ManageUserView.as_view()
        response = view(request, pk=self.user_1.id)

        """
        異常系 1:
        postできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )

    def test_put_user(self):
        url = f"api/agent/v1/user/{self.user_1.id}/"
        data = {
            "id": self.user_1.id,
            "username": "takenaka",
            "name": "takenaka",
            "logo": None,
            "organization_id": self.organization.id,
        }
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user_1)
        view = ManageUserView.as_view()
        response = view(request, pk=self.user_1.id)

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/job_category/{self.user_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user_1)
        view_get = ManageUserView.as_view()
        response_updated_data = view_get(request_updated_data, pk=self.user_1.id)
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            self.user_1.id,
            "id カラムの検証.",
        )
        self.assertEqual(
            updated_data["username"],
            self.user_1.username,
            "username カラムの検証.",
        )
        self.assertEqual(
            updated_data["name"],
            data["name"],
            "name カラムの検証.",
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

    def test_delete_user(self):
        url = f"api/agent/v1/user/{self.user_1.id}/"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user_1)
        view = ManageUserView.as_view()
        response = view(request, pk=self.user_1.id)
        """
        異常系 1:
        削除できないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
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
