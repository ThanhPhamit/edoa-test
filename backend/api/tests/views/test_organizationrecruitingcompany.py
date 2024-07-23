from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories
from api.views import OrganizationCompanyViewSet


class OrganizationCompanyTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.recruiting_company_1 = factories.RecruitingCompanyFactory(name="company1")
        self.recruiting_company_2 = factories.RecruitingCompanyFactory(name="company2")
        self.organization_recruiting_company_1 = factories.OrganizationCompanyFactory(
            recruiting_company_id=self.recruiting_company_1,
            organization_id=self.user.organization_id,
        )
        self.organization_recruiting_company_2 = factories.OrganizationCompanyFactory(
            recruiting_company_id=self.recruiting_company_2,
            organization_id=self.user.organization_id,
        )
        self.organization_recruiting_company_3 = factories.OrganizationCompanyFactory()

    def test_get_organizationrecruitingcompanies(self):
        url = f"api/agent/v1/organization_companies/"
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = OrganizationCompanyViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data["results"]), 2, "2件取得できること.")
        self.assertEqual(data["count"], 2, "2件取得できること.")
        self.assertEqual(
            data["results"][0]["id"],
            str(self.organization_recruiting_company_1.id),
            "id カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["summary"],
            self.organization_recruiting_company_1.summary,
            "summary カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["total_employees"],
            self.organization_recruiting_company_1.total_employees,
            "total_employees カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["profit"],
            self.organization_recruiting_company_1.profit,
            "profit カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["service_years"],
            self.organization_recruiting_company_1.service_years,
            "service_years カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["industry"],
            self.organization_recruiting_company_1.industry,
            "industry カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["salary"],
            self.organization_recruiting_company_1.salary,
            "salary カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["age"],
            self.organization_recruiting_company_1.age,
            "age カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["female_rate"],
            self.organization_recruiting_company_1.female_rate,
            "female_rate カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["disabled_rate"],
            self.organization_recruiting_company_1.disabled_rate,
            "disabled_rate カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["monthly_overtime_hours"],
            self.organization_recruiting_company_1.monthly_overtime_hours,
            "monthly_overtime_hours カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["acquisition_rate"],
            self.organization_recruiting_company_1.acquisition_rate,
            "acquisition_rate カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["childcare_leave_rate"],
            self.organization_recruiting_company_1.childcare_leave_rate,
            "childcare_leave_rate カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["other"],
            self.organization_recruiting_company_1.other,
            "other カラムの検証.",
        )
        self.assertEqual(
            data["results"][0]["recruiting_company_id"]["id"],
            self.organization_recruiting_company_1.recruiting_company_id.id,
            "recruiting_company_id カラムの検証.",
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

    def test_get_organizationrecruitingcompany(self):
        url = f"api/agent/v1/organization_companies/{self.organization_recruiting_company_1.id}/"
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = OrganizationCompanyViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.organization_recruiting_company_1.id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["id"],
            str(self.organization_recruiting_company_1.id),
            "id カラムの検証.",
        )
        self.assertEqual(
            data["summary"],
            self.organization_recruiting_company_1.summary,
            "summary カラムの検証.",
        )
        self.assertEqual(
            data["total_employees"],
            self.organization_recruiting_company_1.total_employees,
            "total_employees カラムの検証.",
        )
        self.assertEqual(
            data["profit"],
            self.organization_recruiting_company_1.profit,
            "profit カラムの検証.",
        )
        self.assertEqual(
            data["service_years"],
            self.organization_recruiting_company_1.service_years,
            "service_years カラムの検証.",
        )
        self.assertEqual(
            data["industry"],
            self.organization_recruiting_company_1.industry,
            "industry カラムの検証.",
        )
        self.assertEqual(
            data["salary"],
            self.organization_recruiting_company_1.salary,
            "salary カラムの検証.",
        )
        self.assertEqual(
            data["age"],
            self.organization_recruiting_company_1.age,
            "age カラムの検証.",
        )
        self.assertEqual(
            data["female_rate"],
            self.organization_recruiting_company_1.female_rate,
            "female_rate カラムの検証.",
        )
        self.assertEqual(
            data["disabled_rate"],
            self.organization_recruiting_company_1.disabled_rate,
            "disabled_rate カラムの検証.",
        )
        self.assertEqual(
            data["monthly_overtime_hours"],
            self.organization_recruiting_company_1.monthly_overtime_hours,
            "monthly_overtime_hours カラムの検証.",
        )
        self.assertEqual(
            data["acquisition_rate"],
            self.organization_recruiting_company_1.acquisition_rate,
            "acquisition_rate カラムの検証.",
        )
        self.assertEqual(
            data["childcare_leave_rate"],
            self.organization_recruiting_company_1.childcare_leave_rate,
            "childcare_leave_rate カラムの検証.",
        )
        self.assertEqual(
            data["other"],
            self.organization_recruiting_company_1.other,
            "other カラムの検証.",
        )
        self.assertEqual(
            data["recruiting_company_id"]["id"],
            self.organization_recruiting_company_1.recruiting_company_id.id,
            "recruiting_company_id カラムの検証.",
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

    def test_post_organizationrecruitingcompany(self):
        url = f"api/agent/v1/organization_companies/"
        data = {
            "summary": "summary",
            "total_employees": 100,
            "profit": 100,
            "service_years": 10,
            "industry": "IT業界",
            "salary": 600,
            "age": 32.5,
            "female_rate": 0.6,
            "disabled_rate": 0.5,
            "monthly_overtime_hours": 24.5,
            "acquisition_rate": 0.7,
            "childcare_leave_rate": 0.2,
            "other": "特になし",
            "recruiting_company_id": {
                "id": self.organization_recruiting_company_1.recruiting_company_id.id
            },
            "tag_id": [],
            "organization_id": {"id": self.user.organization_id.id},
        }

        request = self.factory.post(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = OrganizationCompanyViewSet.as_view({"post": "create"})
        response = view(request)
        data_id = response.data["id"]

        """
        正常系 1:
        正常にデータをpostできること
        """
        url_updated_data = f"api/agent/v1/organization_companies/{data_id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = OrganizationCompanyViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=data_id)
        updated_data = response_updated_data.data

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, "HTTPステータス201が返ること."
        )
        self.assertEqual(
            updated_data["summary"],
            data["summary"],
            "summary カラムの検証.",
        )
        self.assertEqual(
            updated_data["total_employees"],
            data["total_employees"],
            "total_employees カラムの検証.",
        )
        self.assertEqual(
            updated_data["profit"],
            data["profit"],
            "profit カラムの検証.",
        )
        self.assertEqual(
            updated_data["service_years"],
            data["service_years"],
            "service_years カラムの検証.",
        )
        self.assertEqual(
            updated_data["industry"],
            data["industry"],
            "industry カラムの検証.",
        )
        self.assertEqual(
            updated_data["salary"],
            data["salary"],
            "salary カラムの検証.",
        )
        self.assertEqual(
            updated_data["age"],
            data["age"],
            "age カラムの検証.",
        )
        self.assertEqual(
            updated_data["female_rate"],
            data["female_rate"],
            "female_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["disabled_rate"],
            data["disabled_rate"],
            "disabled_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["monthly_overtime_hours"],
            data["monthly_overtime_hours"],
            "monthly_overtime_hours カラムの検証.",
        )
        self.assertEqual(
            updated_data["acquisition_rate"],
            data["acquisition_rate"],
            "acquisition_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["childcare_leave_rate"],
            data["childcare_leave_rate"],
            "childcare_leave_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["other"],
            data["other"],
            "other カラムの検証.",
        )
        self.assertEqual(
            updated_data["recruiting_company_id"]["id"],
            data["recruiting_company_id"]["id"],
            "recruiting_company_id カラムの検証.",
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

    def test_put_organizationrecruitingcompany(self):
        url = f"api/agent/v1/organization_companies/{self.organization_recruiting_company_1.id}/"
        data = {
            "id": self.organization_recruiting_company_1.id,
            "summary": "updatesummary",
            "total_employees": 200,
            "profit": 200,
            "service_years": 20,
            "industry": "製造業",
            "salary": 700,
            "age": 30.5,
            "female_rate": 0.2,
            "disabled_rate": 0.3,
            "monthly_overtime_hours": 22.5,
            "acquisition_rate": 0.5,
            "childcare_leave_rate": 0.1,
            "other": "先進技術に投資",
            "recruiting_company_id": {
                "id": self.organization_recruiting_company_1.recruiting_company_id.id
            },
            "tag_id": [],
            "organization_id": {
                "id": self.organization_recruiting_company_1.organization_id.id
            },
        }
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = OrganizationCompanyViewSet.as_view({"put": "update"})
        response = view(request, pk=self.organization_recruiting_company_1.id)

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/organization_companies/{self.organization_recruiting_company_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = OrganizationCompanyViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(
            request_updated_data, pk=self.organization_recruiting_company_1.id
        )
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            str(data["id"]),
            "id カラムの検証.",
        )
        self.assertEqual(
            updated_data["summary"],
            data["summary"],
            "summary カラムの検証.",
        )
        self.assertEqual(
            updated_data["total_employees"],
            data["total_employees"],
            "total_employees カラムの検証.",
        )
        self.assertEqual(
            updated_data["profit"],
            data["profit"],
            "profit カラムの検証.",
        )
        self.assertEqual(
            updated_data["service_years"],
            data["service_years"],
            "service_years カラムの検証.",
        )
        self.assertEqual(
            updated_data["industry"],
            data["industry"],
            "industry カラムの検証.",
        )
        self.assertEqual(
            updated_data["salary"],
            data["salary"],
            "salary カラムの検証.",
        )
        self.assertEqual(
            updated_data["age"],
            data["age"],
            "age カラムの検証.",
        )
        self.assertEqual(
            updated_data["female_rate"],
            data["female_rate"],
            "female_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["disabled_rate"],
            data["disabled_rate"],
            "disabled_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["monthly_overtime_hours"],
            data["monthly_overtime_hours"],
            "monthly_overtime_hours カラムの検証.",
        )
        self.assertEqual(
            updated_data["acquisition_rate"],
            data["acquisition_rate"],
            "acquisition_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["childcare_leave_rate"],
            data["childcare_leave_rate"],
            "childcare_leave_rate カラムの検証.",
        )
        self.assertEqual(
            updated_data["other"],
            data["other"],
            "other カラムの検証.",
        )
        self.assertEqual(
            updated_data["recruiting_company_id"]["id"],
            data["recruiting_company_id"]["id"],
            "recruiting_company_id カラムの検証.",
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

    def test_delete_organizationrecruitingcompany(self):
        url = f"api/agent/v1/organization_companies/{self.organization_recruiting_company_1.id}/"

        """
        正常系 1:
        正常にデータをdeleteできること
        """
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = OrganizationCompanyViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.organization_recruiting_company_1.id)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, "HTTPステータス204が返ること."
        )

        """
        異常系 1:
        削除されたデータにgetをリクエストした場合、エラーが返ること
        """
        url_updated_data = f"api/agent/v1/organization_companies/{self.organization_recruiting_company_1.id}/"

        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = OrganizationCompanyViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(
            request_updated_data, pk=self.organization_recruiting_company_1.id
        )

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
