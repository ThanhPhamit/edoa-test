from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories
from api.views import RecordBulkUpdateView
import datetime


class RecordBulkUpdateTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.record_1 = factories.RecordFactory(
            organization_id=self.user.organization_id,
        )
        self.record_2 = factories.RecordFactory(
            organization_id=self.user.organization_id,
        )
        self.record_3 = factories.RecordFactory()

    def test_get_records(self):
        url = f"api/agent/v1/records/bulk_update/"
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = RecordBulkUpdateView.as_view()
        response = view(request)

        """
        異常系 1:
        getできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )

    def test_get_record(self):
        url = f"api/agent/v1/records/bulk_update/{self.record_1.id}/"
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = RecordBulkUpdateView.as_view()
        response = view(request, pk=self.record_1.id)

        """
        異常系 1:
        getできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )

    def test_post_records(self):
        url = f"api/agent/v1/records/bulk_update/"
        data = [
            {
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
        ]
        request = self.factory.post(
            url,
            data=data,
            format="json",
        )

        force_authenticate(request, user=self.user)
        view = RecordBulkUpdateView.as_view()
        response = view(request)

        """
        異常系 1:
        postできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )

    def test_put_records(self):
        url = f"api/agent/v1/records/bulk_update/"
        data = [
            {
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
            },
            {
                "id": self.record_2.id,
                "proposal_id": {
                    "id": self.record_2.proposal_id.id,
                    "jobseeker_id": {
                        "id": self.record_2.proposal_id.jobseeker_id.id,
                        "name": "yamamoto",
                        "birth_date": "2023-05-02",
                        "gender": "female",
                        "phone_number": "11112345678",
                        "in_charge_id": {"id": self.user.id},
                        "last_record_at": "2023-06-02T13:49:37+09:00",
                    },
                    "job_id": {
                        "id": self.record_2.proposal_id.job_id.id,
                        "recruiting_company_id": {
                            "id": self.record_2.proposal_id.job_id.recruiting_company_id.id
                        },
                        "job_category_id": {
                            "id": self.record_2.proposal_id.job_id.job_category_id.id
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
            },
        ]
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )

        force_authenticate(request, user=self.user)
        view = RecordBulkUpdateView.as_view()
        response = view(request, pk=self.record_1.id)

        """
        正常系 1:
        正常にデータをputできること
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")

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

    def test_delete_record(self):
        url = f"api/agent/v1/records/bulk_update/{self.record_1.id}/"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = RecordBulkUpdateView.as_view()
        response = view(request, pk=self.record_1.id)

        """
        異常系 1:
        deleteできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )
