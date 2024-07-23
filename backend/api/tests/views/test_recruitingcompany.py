from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from datetime import datetime
from api.tests import factories

from api.views import RecruitingCompanyViewSet


class RecruitingCompanyTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.organization = factories.OrganizationFactory(name="test")
        self.user = factories.UserFactory()
        self.recruiting_companies = []
        for i in range(5) :
            self.recruiting_companies.append(factories.RecruitingCompanyFactory(name=f"company{i}"))
            self.recruiting_companies.append(factories.RecruitingCompanyFactory(name=f"querytargetcompany{i}"))

    def test_get_recruiting_companies(self):
        url = "".join([reverse("agent_recmii:recruitingcompany-list"), "?top=100"])
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = RecruitingCompanyViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data), 10, "10件取得できること.")
        self.assertEqual(
            data[0]["id"],
            self.recruiting_companies[0].id,
            "id カラムの検証.",
        )
        self.assertEqual(
            data[0]["corporate_number"],
            self.recruiting_companies[0].corporate_number,
            "corporate_number カラムの検証.",
        )
        self.assertEqual(
            data[0]["name"],
            self.recruiting_companies[0].name,
            "name カラムの検証.",
        )
        self.assertEqual(
            data[0]["company_url"],
            self.recruiting_companies[0].company_url,
            "company_url カラムの検証.",
        )
        self.assertEqual(
            data[0]["recruiting_url"],
            self.recruiting_companies[0].recruiting_url,
            "recruiting_url カラムの検証.",
        )
        self.assertEqual(
            data[0]["logo"],
            self.recruiting_companies[0].logo,
            "logo カラムの検証.",
        )
        self.assertEqual(
            data[0]["establishment_date"],
            self.recruiting_companies[0].establishment_date,
            "establishment_date カラムの検証.",
        )
        self.assertEqual(
            data[0]["is_listed"],
            self.recruiting_companies[0].is_listed,
            "is_listed カラムの検証.",
        )

        """
        正常系 2:
        パラメータtopで指定した件数のデータをgetできること
        """
        url_top = "".join([reverse("agent_recmii:recruitingcompany-list"), "?top=3"])
        request_top = self.factory.get(url_top)
        force_authenticate(request_top, user=self.user)
        view_top = RecruitingCompanyViewSet.as_view({"get": "list"})
        response_top = view_top(request_top)
        data_top = response_top.data

        self.assertEqual(response_top.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data_top), 3, "3件のみ取得できること.")

        """
        正常系 3:
        パラメータqで指定した文字列を含むデータをgetできること
        """
        url_q = "".join([reverse("agent_recmii:recruitingcompany-list"), "?q=target", "&top=100"])
        request_q = self.factory.get(url_q)
        force_authenticate(request_q, user=self.user)
        view_q = RecruitingCompanyViewSet.as_view({"get": "list"})
        response_q = view_q(request_q)
        data_q = response_q.data

        self.assertEqual(response_q.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data_q), 5, "5件のみ取得できること.")

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

        """
        異常系 2:
        パラメータtopが存在しないとき、エラーが返ること
        """
        url_no_top = "".join([reverse("agent_recmii:recruitingcompany-list")])
        request_no_top = self.factory.get(url_no_top)
        force_authenticate(request_no_top, user=self.user)
        view_no_top = RecruitingCompanyViewSet.as_view({"get": "list"})
        response_no_top = view_no_top(request_no_top)

        self.assertEqual(
            response_no_top.status_code,
            status.HTTP_400_BAD_REQUEST,
            "HTTPステータス400が返ること.",
        )

        """
        異常系 3:
        パラメータtopが数でないとき、エラーが返ること
        """
        url_not_int_top = "".join([reverse("agent_recmii:recruitingcompany-list"), "&top=aaa"])
        request_not_int_top = self.factory.get(url_not_int_top)
        force_authenticate(request_not_int_top, user=self.user)
        view_not_int_top = RecruitingCompanyViewSet.as_view({"get": "list"})
        response_not_int_top = view_not_int_top(request_not_int_top)

        self.assertEqual(
            response_not_int_top.status_code,
            status.HTTP_400_BAD_REQUEST,
            "HTTPステータス400が返ること.",
        )

    def test_get_recruiting_company(self):
        url = f"api/agent/v1/recruiting_companies/{self.recruiting_companies[0].id}/"
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = RecruitingCompanyViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.recruiting_companies[0].id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["id"],
            self.recruiting_companies[0].id,
            "id カラムの検証.",
        )
        self.assertEqual(
            data["corporate_number"],
            self.recruiting_companies[0].corporate_number,
            "corporate_number カラムの検証.",
        )
        self.assertEqual(
            data["name"],
            self.recruiting_companies[0].name,
            "name カラムの検証.",
        )
        self.assertEqual(
            data["company_url"],
            self.recruiting_companies[0].company_url,
            "company_url カラムの検証.",
        )
        self.assertEqual(
            data["recruiting_url"],
            self.recruiting_companies[0].recruiting_url,
            "recruiting_url カラムの検証.",
        )
        self.assertEqual(
            data["logo"],
            self.recruiting_companies[0].logo,
            "logo カラムの検証.",
        )
        self.assertEqual(
            data["establishment_date"],
            self.recruiting_companies[0].establishment_date,
            "establishment_date カラムの検証.",
        )
        self.assertEqual(
            data["is_listed"],
            self.recruiting_companies[0].is_listed,
            "is_listed カラムの検証.",
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

    def test_post_recruiting_company(self):
        url = "".join([reverse("agent_recmii:recruitingcompany-list")])
        request = self.factory.post(
            url,
            data={
                "id": 3,
                "corporate_number": "0123456789000",
                "name": "apple",
                "company_url": "https//apple.com",
                "recruiting_url": "https//apple.com/recruit",
                "logo": None,
                "establishment_date": datetime.strptime("20210501", "%Y%m%d"),
                "is_listed": datetime.strptime("20210601", "%Y%m%d"),
            },
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = RecruitingCompanyViewSet.as_view({"post": "create"})
        response = view(request)
        data_id = response.data["id"]

        """
        正常系 1:
        正常にデータをpostできること
        """
        url_updated_data = f"api/agent/v1/jobs/{data_id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = RecruitingCompanyViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=data_id)
        updated_data = response_updated_data.data

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, "HTTPステータス201が返ること."
        )
        self.assertEqual(
            updated_data["id"],
            3,
            "id カラムの検証.",
        )
        self.assertEqual(
            updated_data["corporate_number"],
            "",
            "corporate_number カラムの検証.",
        )
        self.assertEqual(
            updated_data["name"],
            "",
            "name カラムの検証.",
        )
        self.assertEqual(
            updated_data["company_url"],
            "",
            "company_url カラムの検証.",
        )
        self.assertEqual(
            updated_data["recruiting_url"],
            "",
            "recruiting_url カラムの検証.",
        )
        self.assertEqual(
            updated_data["logo"],
            None,
            "logo カラムの検証.",
        )
        self.assertEqual(
            updated_data["establishment_date"],
            None,
            "establishment_date カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_listed"],
            None,
            "is_listed カラムの検証.",
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

    def test_put_recruiting_company(self):
        url = f"api/agent/v1/recruiting_companies/{self.recruiting_companies[0].id}/"
        request = self.factory.put(
            url,
            data={
                "id": self.recruiting_companies[0].id,
                "corporate_number": "0123456789999",
                "name": "facebook",
                "company_url": "https//facebook.com",
                "recruiting_url": "https//facebook.com/recruit",
                "logo": None,
                "establishment_date": datetime.strptime("20230502", "%Y%m%d"),
                "is_listed": datetime.strptime("20230602", "%Y%m%d"),
            },
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = RecruitingCompanyViewSet.as_view({"put": "update"})
        response = view(request, pk=self.recruiting_companies[0].id)

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/jobs/{self.recruiting_companies[0].id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = RecruitingCompanyViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(
            request_updated_data, pk=self.recruiting_companies[0].id
        )
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            self.recruiting_companies[0].id,
            "id カラムの検証.",
        )
        self.assertEqual(
            updated_data["corporate_number"],
            self.recruiting_companies[0].corporate_number,
            "corporate_number カラムの検証.",
        )
        self.assertEqual(
            updated_data["name"],
            self.recruiting_companies[0].name,
            "name カラムの検証.",
        )
        self.assertEqual(
            updated_data["company_url"],
            self.recruiting_companies[0].company_url,
            "company_url カラムの検証.",
        )
        self.assertEqual(
            updated_data["recruiting_url"],
            self.recruiting_companies[0].recruiting_url,
            "recruiting_url カラムの検証.",
        )
        self.assertEqual(
            updated_data["logo"],
            None,
            "logo カラムの検証.",
        )
        self.assertEqual(
            updated_data["establishment_date"],
            self.recruiting_companies[0].establishment_date,
            "establishment_date カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_listed"],
            self.recruiting_companies[0].is_listed,
            "is_listed カラムの検証.",
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

    def test_delete_recruiting_company(self):
        url = f"api/agent/v1/recruiting_companies/{self.recruiting_companies[0].id}/"

        """
        正常系 1:
        正常にデータをdeleteできること
        """
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = RecruitingCompanyViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.recruiting_companies[0].id)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, "HTTPステータス204が返ること."
        )
        """
        異常系 1:
        削除されたデータにgetをリクエストした場合、エラーが返ること
        """
        url_updated_data = f"api/agent/v1/jobs/{self.recruiting_companies[0].id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = RecruitingCompanyViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(
            request_updated_data, pk=self.recruiting_companies[0].id
        )

        self.assertEqual(
            response_updated_data.status_code,
            status.HTTP_404_NOT_FOUND,
            "HTTPステータス404が返ること.",
        )
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
