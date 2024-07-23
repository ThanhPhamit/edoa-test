from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories
from api.views import JobViewSet


class JobTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.job_1 = factories.JobFactory(organization_id=self.user.organization_id)
        self.job_2 = factories.JobFactory(organization_id=self.user.organization_id)
        self.job_3 = factories.JobFactory()

    def test_get_jobs(self):
        url = "".join([reverse("agent_recmii:job-list")])
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data["results"]), 2, "2件取得できること.")
        self.assertEqual(data["count"], 2, "2件取得できること.")

        self.assertEqual(data["results"][0]["id"], str(self.job_2.id), "id カラムの検証")
        self.assertEqual(
            data["results"][0]["recruiting_company_id"]["id"],
            self.job_2.recruiting_company_id.id,
            "recruiting_company_id id カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["job_category_id"]["id"],
            str(self.job_2.job_category_id.id),
            "job_category_id id カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["position"], self.job_2.position, "position カラムの検証"
        )
        self.assertEqual(data["results"][0]["layer"], self.job_2.layer, "layer カラムの検証")
        self.assertEqual(
            data["results"][0]["min_salary"], self.job_2.min_salary, "min_salary カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["max_salary"], self.job_2.max_salary, "max_salary カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["salary"], self.job_2.salary, "salary カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["employment_status"],
            self.job_2.employment_status,
            "employment_status カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["summary"], self.job_2.summary, "summary カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["min_qualifications"],
            self.job_2.min_qualifications,
            "min_qualifications カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["pfd_qualifications"],
            self.job_2.pfd_qualifications,
            "pfd_qualifications カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["ideal_profile"],
            self.job_2.ideal_profile,
            "ideal_profile カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["address"], self.job_2.address, "address カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["remote"], self.job_2.remote, "remote カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["working_hours"],
            self.job_2.working_hours,
            "working_hours カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["holiday"], self.job_2.holiday, "holiday カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["benefit"], self.job_2.benefit, "benefit カラムの検証"
        )
        self.assertEqual(
            data["results"][0]["trial_period"],
            self.job_2.trial_period,
            "trial_period カラムの検証",
        )
        self.assertEqual(
            data["results"][0]["smoking_prevention_measure"],
            self.job_2.smoking_prevention_measure,
            "smoking_prevention_measure カラムの検証",
        )
        self.assertEqual(data["results"][0]["other"], self.job_2.other, "other カラムの検証")

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

    def test_search_jobs_name(self):
        keyword = self.job_1.recruiting_company_id.name[0:3]
        url = "".join([reverse("agent_recmii:job-list")]) + f"?keyword={keyword}"

        """
        正常系 1:
        recruiting_company_idのnameで前方一致検索され正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data["results"]), 1, "1件取得できること.")
        self.assertEqual(data["count"], 1, "1件取得できること.")
        self.assertEqual(data["results"][0]["id"], str(self.job_1.id), "id カラムの検証")

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

    def test_search_jobs_position(self):
        keyword = self.job_1.position[0:3]
        url = "".join([reverse("agent_recmii:job-list")]) + f"?keyword={keyword}"

        """
        正常系 1:
        positionで前方一致検索され正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data["results"]), 1, "1件取得できること.")
        self.assertEqual(data["count"], 1, "1件取得できること.")
        self.assertEqual(data["results"][0]["id"], str(self.job_1.id), "id カラムの検証")

        """
        異常系 1:
        認証されていないユーザーgetをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.get(url)
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(
            reponse_unauthorize.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "HTTPステータス401が返ること.",
        )

    def test_get_job(self):
        url = f"api/agent/v1/jobs/{self.job_1.id}/"

        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = JobViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.job_1.id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["id"],
            str(self.job_1.id),
            "id カラムの検証",
        )
        self.assertEqual(
            data["recruiting_company_id"]["id"],
            self.job_1.recruiting_company_id.id,
            "recruiting_company_id id カラムの検証",
        )
        self.assertEqual(
            data["job_category_id"]["id"],
            str(self.job_1.job_category_id.id),
            "job_category_id id カラムの検証",
        )
        self.assertEqual(data["position"], self.job_1.position, "position カラムの検証")
        self.assertEqual(data["layer"], self.job_1.layer, "layer カラムの検証")
        self.assertEqual(
            data["min_salary"],
            self.job_1.min_salary,
            "min_salary カラムの検証",
        )
        self.assertEqual(
            data["max_salary"],
            self.job_1.max_salary,
            "max_salary カラムの検証",
        )
        self.assertEqual(
            data["salary"],
            self.job_1.salary,
            "salary カラムの検証",
        )
        self.assertEqual(
            data["employment_status"],
            self.job_1.employment_status,
            "employment_status カラムの検証",
        )
        self.assertEqual(
            data["summary"],
            self.job_1.summary,
            "summary カラムの検証",
        )
        self.assertEqual(
            data["min_qualifications"],
            self.job_1.min_qualifications,
            "min_qualifications カラムの検証",
        )
        self.assertEqual(
            data["pfd_qualifications"],
            self.job_1.pfd_qualifications,
            "pfd_qualifications カラムの検証",
        )
        self.assertEqual(
            data["ideal_profile"],
            self.job_1.ideal_profile,
            "ideal_profile カラムの検証",
        )
        self.assertEqual(
            data["address"],
            self.job_1.address,
            "address カラムの検証",
        )
        self.assertEqual(data["remote"], self.job_1.remote, "remote カラムの検証")
        self.assertEqual(
            data["working_hours"],
            self.job_1.working_hours,
            "working_hours カラムの検証",
        )
        self.assertEqual(
            data["holiday"],
            self.job_1.holiday,
            "holiday カラムの検証",
        )
        self.assertEqual(
            data["benefit"],
            self.job_1.benefit,
            "benefit カラムの検証",
        )
        self.assertEqual(
            data["trial_period"],
            self.job_1.trial_period,
            "trial_period カラムの検証",
        )
        self.assertEqual(
            data["smoking_prevention_measure"],
            self.job_1.smoking_prevention_measure,
            "smoking_prevention_measure カラムの検証",
        )
        self.assertEqual(
            data["other"],
            self.job_1.other,
            "other カラムの検証",
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

    def test_post_jobs(self):
        url = "".join([reverse("agent_recmii:job-list")])
        data = {
            "recruiting_company_id": {"id": self.job_1.recruiting_company_id.id},
            "job_category_id": {"id": self.job_1.job_category_id.id},
            "position": "salesmanager",
            "layer": "manager",
            "min_salary": "5000000",
            "max_salary": "80000000",
            "salary": "月20時間残業代込み",
            "employment_status": "sub",
            "summary": "セールスマネジメント",
            "min_qualifications": "セールス経験",
            "pfd_qualifications": "10人規模のマネジメント経験",
            "ideal_profile": "周囲を巻き込む力",
            "address": "神奈川県",
            "remote": "full",
            "working_hours": "一部リモート",
            "holiday": "日月",
            "benefit": "賞与あり",
            "trial_period": "3ヶ月",
            "smoking_prevention_measure": "屋内禁煙",
            "other": "託児所あり",
        }
        request = self.factory.post(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = JobViewSet.as_view({"post": "create"})
        response = view(request)
        data_id = response.data["id"]

        """
        正常系 1:
        正常にデータをpostできること
        """
        url_updated_data = f"api/agent/v1/jobs/{data_id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = JobViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=data_id)
        updated_data = response_updated_data.data

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, "HTTPステータス201が返ること."
        )

        self.assertEqual(
            updated_data["id"],
            str(data_id),
            "id カラムの検証",
        )
        self.assertEqual(
            updated_data["recruiting_company_id"]["id"],
            data["recruiting_company_id"]["id"],
            "recruiting_company_id id カラムの検証",
        )
        self.assertEqual(
            updated_data["job_category_id"]["id"],
            str(data["job_category_id"]["id"]),
            "job_category_id id カラムの検証",
        )
        self.assertEqual(updated_data["position"], "salesmanager", "position カラムの検証")
        self.assertEqual(updated_data["layer"], "manager", "layer カラムの検証")
        self.assertEqual(
            updated_data["min_salary"],
            data["min_salary"],
            "min_salary カラムの検証",
        )
        self.assertEqual(
            updated_data["max_salary"],
            data["max_salary"],
            "max_salary カラムの検証",
        )
        self.assertEqual(
            updated_data["salary"],
            data["salary"],
            "salary カラムの検証",
        )
        self.assertEqual(
            updated_data["employment_status"],
            data["employment_status"],
            "employment_status カラムの検証",
        )
        self.assertEqual(
            updated_data["summary"],
            data["summary"],
            "summary カラムの検証",
        )
        self.assertEqual(
            updated_data["min_qualifications"],
            data["min_qualifications"],
            "min_qualifications カラムの検証",
        )
        self.assertEqual(
            updated_data["pfd_qualifications"],
            data["pfd_qualifications"],
            "pfd_qualifications カラムの検証",
        )
        self.assertEqual(
            updated_data["ideal_profile"],
            data["ideal_profile"],
            "ideal_profile カラムの検証",
        )
        self.assertEqual(
            updated_data["address"],
            data["address"],
            "address カラムの検証",
        )
        self.assertEqual(updated_data["remote"], "full", "remote カラムの検証")
        self.assertEqual(
            updated_data["working_hours"],
            data["working_hours"],
            "working_hours カラムの検証",
        )
        self.assertEqual(
            updated_data["holiday"],
            data["holiday"],
            "holiday カラムの検証",
        )
        self.assertEqual(
            updated_data["benefit"],
            data["benefit"],
            "benefit カラムの検証",
        )
        self.assertEqual(
            updated_data["trial_period"],
            data["trial_period"],
            "trial_period カラムの検証",
        )
        self.assertEqual(
            updated_data["smoking_prevention_measure"],
            data["smoking_prevention_measure"],
            "smoking_prevention_measure カラムの検証",
        )
        self.assertEqual(
            updated_data["other"],
            data["other"],
            "other カラムの検証",
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

    def test_put_jobs(self):
        url = f"api/agent/v1/jobs/{self.job_1.id}/"
        data = {
            "id": self.job_1.id,
            "recruiting_company_id": {"id": self.job_1.recruiting_company_id.id},
            "job_category_id": {"id": self.job_1.job_category_id.id},
            "position": "salesmanager",
            "layer": "manager",
            "min_salary": "5000000",
            "max_salary": "80000000",
            "salary": "月20時間残業代込み",
            "employment_status": "sub",
            "summary": "セールスマネジメント",
            "min_qualifications": "セールス経験",
            "pfd_qualifications": "10人規模のマネジメント経験",
            "ideal_profile": "周囲を巻き込む力",
            "address": "神奈川県",
            "remote": "full",
            "working_hours": "一部リモート",
            "holiday": "日月",
            "benefit": "賞与あり",
            "trial_period": "5ヶ月",
            "smoking_prevention_measure": "屋内喫煙",
            "other": "託児所あり",
        }
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = JobViewSet.as_view({"put": "update"})
        response = view(request, pk=self.job_1.id)

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/jobs/{self.job_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = JobViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.job_1.id)
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            str(self.job_1.id),
            "id カラムの検証",
        )
        self.assertEqual(
            updated_data["recruiting_company_id"]["id"],
            data["recruiting_company_id"]["id"],
            "recruiting_company_id id カラムの検証",
        )
        self.assertEqual(
            updated_data["job_category_id"]["id"],
            str(data["job_category_id"]["id"]),
            "job_category_id id カラムの検証",
        )
        self.assertEqual(updated_data["position"], data["position"], "position カラムの検証")
        self.assertEqual(updated_data["layer"], data["layer"], "layer カラムの検証")
        self.assertEqual(
            updated_data["min_salary"],
            data["min_salary"],
            "min_salary カラムの検証",
        )
        self.assertEqual(
            updated_data["max_salary"],
            data["max_salary"],
            "max_salary カラムの検証",
        )
        self.assertEqual(
            updated_data["salary"],
            data["salary"],
            "salary カラムの検証",
        )
        self.assertEqual(
            updated_data["employment_status"],
            data["employment_status"],
            "employment_status カラムの検証",
        )
        self.assertEqual(
            updated_data["summary"],
            data["summary"],
            "summary カラムの検証",
        )
        self.assertEqual(
            updated_data["min_qualifications"],
            data["min_qualifications"],
            "min_qualifications カラムの検証",
        )
        self.assertEqual(
            updated_data["pfd_qualifications"],
            data["pfd_qualifications"],
            "pfd_qualifications カラムの検証",
        )
        self.assertEqual(
            updated_data["ideal_profile"],
            data["ideal_profile"],
            "ideal_profile カラムの検証",
        )
        self.assertEqual(
            updated_data["address"],
            data["address"],
            "address カラムの検証",
        )
        self.assertEqual(updated_data["remote"], data["remote"], "remote カラムの検証")
        self.assertEqual(
            updated_data["working_hours"],
            data["working_hours"],
            "working_hours カラムの検証",
        )
        self.assertEqual(
            updated_data["holiday"],
            data["holiday"],
            "holiday カラムの検証",
        )
        self.assertEqual(
            updated_data["benefit"],
            data["benefit"],
            "benefit カラムの検証",
        )
        self.assertEqual(
            updated_data["trial_period"],
            data["trial_period"],
            "trial_period カラムの検証",
        )
        self.assertEqual(
            updated_data["smoking_prevention_measure"],
            data["smoking_prevention_measure"],
            "smoking_prevention_measure カラムの検証",
        )
        self.assertEqual(
            updated_data["other"],
            data["other"],
            "other カラムの検証",
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

    def test_delete_job(self):
        """
        正常系 1:
        正常にデータをdeleteできること
        """
        url = f"api/agent/v1/jobs/{self.job_1.id}/"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = JobViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.job_1.id)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, "HTTPステータス204が返ること."
        )

        """
        異常系 1:
        削除されたデータにgetをリクエストした場合、エラーが返ること
        """
        url_updated_data = f"api/agent/v1/jobs/{self.job_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = JobViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.job_1.id)

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
