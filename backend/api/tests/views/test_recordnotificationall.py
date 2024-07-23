from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

import datetime
from api.tests import factories
from api.views import RecordNotificationAllViewSet


class RecordNotificationAllTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.jobseeker = factories.JobseekerFactory(
            in_charge_id=self.user,
            organization_id=self.user.organization_id,
        )
        self.proposal = factories.ProposalFactory(
            jobseeker_id=self.jobseeker,
            organization_id=self.user.organization_id,
        )
        self.record_1 = factories.RecordFactory(
            is_long_time=False,
            is_checked=False,
            proposal_id=self.proposal,
            organization_id=self.user.organization_id,
        )
        self.record_2 = factories.RecordFactory(
            is_long_time=True,
            is_checked=True,
            proposal_id=self.proposal,
            organization_id=self.user.organization_id,
        )
        self.record_3 = factories.RecordFactory(
            is_long_time=False,
            is_checked=False,
        )

    def test_get_records(self):
        url = "api/agent/v1/notifications/record/all/"
        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = RecordNotificationAllViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data), 1, "1件取得できること.")

        self.assertEqual(
            data[0]["id"],
            str(self.record_1.id),
            "id カラムの検証.",
        )
        self.assertEqual(
            data[0]["before_record_at"],
            self.record_1.before_record_at.astimezone(
                datetime.timezone(datetime.timedelta(hours=9))
            ).isoformat(),
            "before_record_at カラムの検証.",
        )
        self.assertEqual(
            data[0]["is_long_time"],
            self.record_1.is_long_time,
            "is_long_time カラムの検証.",
        )
        self.assertEqual(
            data[0]["is_checked"],
            self.record_1.is_checked,
            "is_checked カラムの検証.",
        )
        self.assertEqual(
            data[0]["trigger"],
            self.record_1.trigger,
            "trigger カラムの検証.",
        )
        self.assertEqual(
            data[0]["proposal_id"]["id"],
            str(self.record_1.proposal_id.id),
            "proposal_id id カラムの検証.",
        )

        """
        異常系 1:
        パスワードを読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data[0]["proposal_id"]["jobseeker_id"]["in_charge_id"]["password"]

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

    def test_search_jobseeker_id(self):
        keyword = self.record_1.proposal_id.jobseeker_id.id
        url = "api/agent/v1/notifications/record/all/" + f"?keyword={keyword}"

        """
        正常系 1:
        recruiting_company_idのnameで前方一致検索され正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = RecordNotificationAllViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data), 1, "1件取得できること.")
        self.assertEqual(
            data[0]["id"],
            str(self.record_1.id),
            "id カラムの検証",
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

    def test_get_record(self):
        url = f"api/agent/v1/notifications/record/all/{self.record_1.id}/"

        """
        正常系 1:
        正常にデータをgetできること
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = RecordNotificationAllViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.record_1.id)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["id"],
            str(self.record_1.id),
            "id カラムの検証.",
        )
        self.assertEqual(
            data["before_record_at"],
            self.record_1.before_record_at.astimezone(
                datetime.timezone(datetime.timedelta(hours=9))
            ).isoformat(),
            "before_record_at カラムの検証.",
        )
        self.assertEqual(
            data["is_long_time"],
            self.record_1.is_long_time,
            "is_long_time カラムの検証.",
        )
        self.assertEqual(
            data["is_checked"],
            self.record_1.is_checked,
            "is_checked カラムの検証.",
        )
        self.assertEqual(
            data["trigger"],
            self.record_1.trigger,
            "trigger カラムの検証.",
        )
        self.assertEqual(
            data["proposal_id"]["id"],
            str(self.record_1.proposal_id.id),
            "proposal_id id カラムの検証.",
        )

        """
        異常系 1:
        パスワードを読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data["proposal_id"]["jobseeker_id"]["in_charge_id"]["password"]

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

    def test_post_records(self):
        url = "api/agent/v1/notifications/record/all/"
        data = {
            "id": self.record_1.id,
            "proposal_id": {
                "id": self.record_1.proposal_id.id,
                "jobseeker_id": {
                    "id": self.record_1.proposal_id.jobseeker_id.id,
                    "name": "yamamoto",
                    "birth_date": "2023-05-02",
                    "gender": "female",
                    "phone_number": "11112345678",
                    "in_charge_id": {"id": self.user.id},
                    "last_record_at": "2023-06-02T13:49:37+09:00",
                },
                "job_id": {
                    "id": self.record_1.proposal_id.job_id.id,
                    "recruiting_company_id": {
                        "id": self.record_1.proposal_id.job_id.recruiting_company_id.id
                    },
                    "job_category_id": {
                        "id": self.record_1.proposal_id.job_id.job_category_id.id
                    },
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
                    "other": "託児所あり",
                },
                "intention": "3",
                "is_favorite": False,
                "comment": "おすすめできます",
                "is_public": False,
                "position": "engineermanager",
                "salary": "月30時間残業代込み",
                "summary": "バックエンドエンジニア",
                "min_qualifications": "開発経験",
                "pfd_qualifications": "自社開発経験",
                "ideal_profile": "整理できる方",
                "tag_id": [],
                "is_appeal_layer": False,
                "is_appeal_remote": False,
                "organization_id": {"id": self.user.organization_id.id},
            },
            "before_record_at": "2023-06-02T13:49:37+09:00",
            "is_long_time": True,
            "is_checked": True,
            "trigger": "detail_view",
        }
        request = self.factory.post(
            url,
            data=data,
            format="json",
        )

        force_authenticate(request, user=self.user)
        view = RecordNotificationAllViewSet.as_view({"post": "create"})

        """
        異常系 1:
        postできないこと
        """
        with self.assertRaises(AttributeError) as raises:
            view(request)

    def test_put_records(self):
        url = f"api/agent/v1/notifications/record/all/{self.record_1.id}/"
        data = {
            "id": self.record_1.id,
            "proposal_id": {
                "id": self.record_1.proposal_id.id,
                "jobseeker_id": {
                    "id": self.record_1.proposal_id.jobseeker_id.id,
                    "name": "yamamoto",
                    "birth_date": "2023-05-02",
                    "gender": "female",
                    "phone_number": "11112345678",
                    "in_charge_id": {"id": self.user.id},
                    "last_record_at": "2023-06-02T13:49:37+09:00",
                },
                "job_id": {
                    "id": self.record_1.proposal_id.job_id.id,
                    "recruiting_company_id": {
                        "id": self.record_1.proposal_id.job_id.recruiting_company_id.id
                    },
                    "job_category_id": {
                        "id": self.record_1.proposal_id.job_id.job_category_id.id
                    },
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
                    "other": "託児所あり",
                },
                "intention": "3",
                "is_favorite": False,
                "comment": "おすすめできます",
                "is_public": False,
                "position": "engineermanager",
                "salary": "月30時間残業代込み",
                "summary": "バックエンドエンジニア",
                "min_qualifications": "開発経験",
                "pfd_qualifications": "自社開発経験",
                "ideal_profile": "整理できる方",
                "tag_id": [],
                "is_appeal_layer": False,
                "is_appeal_remote": False,
                "organization_id": {"id": self.user.organization_id.id},
            },
            "before_record_at": "2023-06-02T13:49:37+09:00",
            "is_long_time": True,
            "is_checked": False,
            "trigger": "detail_view",
        }
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = RecordNotificationAllViewSet.as_view({"put": "update"})
        response = view(request, pk=self.record_1.id)

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/notifications/record/all/{self.record_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = RecordNotificationAllViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.record_1.id)
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["id"],
            str(self.record_1.id),
            "id カラムの検証.",
        )
        self.assertEqual(
            updated_data["before_record_at"],
            data["before_record_at"],
            "before_record_at カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_long_time"],
            data["is_long_time"],
            "is_long_time カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_checked"],
            data["is_checked"],
            "is_checked カラムの検証.",
        )
        self.assertEqual(
            updated_data["trigger"],
            data["trigger"],
            "trigger カラムの検証.",
        )
        self.assertEqual(
            updated_data["proposal_id"]["id"],
            str(data["proposal_id"]["id"]),
            "proposal_id id カラムの検証.",
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

    def test_delete_record(self):
        """
        正常系 1:
        正常にデータをdeleteできること
        """
        url = f"api/agent/v1/notifications/record/all/{self.record_1.id}/"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = RecordNotificationAllViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.record_1.id)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, "HTTPステータス204が返ること."
        )

        """
        異常系 1:
        削除されたデータにgetをリクエストした場合、エラーが返ること
        """
        url_updated_data = f"api/agent/v1/notifications/record/all/{self.record_1.id}/"
        request_updated_data = self.factory.get(url_updated_data)
        force_authenticate(request_updated_data, user=self.user)
        view_get = RecordNotificationAllViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.record_1.id)

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
