from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories
from api.views import TagViewSet


class TagTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.tag_1 = factories.TagFactory(
            organization_id=self.user.organization_id,
        )
        self.tag_2 = factories.TagFactory(
            organization_id=self.user.organization_id,
        )
        self.tag_3 = factories.TagFactory()

    def test_get_tags(self):
        url = f"api/agent/v1/tags/"
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = TagViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data), 2, "2件取得できること.")
        self.assertEqual(
            data[0]["id"],
            str(self.tag_1.id),
            "id カラムの検証.",
        )
        self.assertEqual(
            data[0]["name"],
            self.tag_1.name,
            "name カラムの検証.",
        )

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

    def test_get_tag(self):
        url = f"api/agent/v1/tags/{self.tag_1.id}/"
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = TagViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.tag_1.id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["id"],
            str(self.tag_1.id),
            "id カラムの検証.",
        )
        self.assertEqual(
            data["name"],
            self.tag_1.name,
            "name カラムの検証.",
        )

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

    def test_post_tag(self):
        url = f"api/agent/v1/tags/"
        data = {
            "name": "name",
            "organization_id": {"id": self.user.organization_id.id},
        }

        request = self.factory.post(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = TagViewSet.as_view({"post": "create"})
        response = view(request)
        data_id = response.data["id"]

        """
        正常系 1:
        正常にデータをpostできること
        """
        url_updated_data = f"api/agent/v1/tags/{data_id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = TagViewSet.as_view({"get": "retrieve"})
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
        self.assertEqual(
            updated_data["name"],
            data["name"],
            "name カラムの検証.",
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

    def test_put_tag(self):
        url = f"api/agent/v1/tags/{self.tag_1.id}/"
        data = {
            "id": self.tag_1.id,
            "name": "namename",
            "organization_id": {"id": self.user.organization_id.id},
        }
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = TagViewSet.as_view({"put": "update"})
        response = view(request, pk=self.tag_1.id)

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/tags/{self.tag_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = TagViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.tag_1.id)
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            str(data["id"]),
            "id カラムの検証.",
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

    def test_delete_tag(self):
        url = f"api/agent/v1/tags/{self.tag_1.id}/"

        """
        正常系 1:
        正常にデータをdeleteできること
        """
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = TagViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.tag_1.id)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, "HTTPステータス204が返ること."
        )

        """
        異常系 1:
        削除されたデータにgetをリクエストした場合、エラーが返ること
        """
        url_updated_data = f"api/agent/v1/tags/{self.tag_1.id}/"

        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = TagViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.tag_1.id)

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
