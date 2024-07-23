from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories

from api.views import ProposalBulkCreateView


class ProposalBulkCreateTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.proposal_1 = factories.ProposalFactory(
            organization_id=self.user.organization_id,
        )
        self.proposal_2 = factories.ProposalFactory(
            organization_id=self.user.organization_id,
        )
        self.proposal_3 = factories.ProposalFactory()

    def test_get_proposals(self):
        url = "".join([reverse("agent_recmii:proposal-list")])
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = ProposalBulkCreateView.as_view()
        response = view(request)
        data = response.data

        """
        異常系 1:
        getできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )

    def test_get_proposal(self):
        url = f"api/agent/v1/proposals/{self.proposal_1.id}/"
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        view = ProposalBulkCreateView.as_view()
        response = view(request, pk=self.proposal_1.id)
        data = response.data

        """
        異常系 1:
        getできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )

    def test_post_proposals(self):
        url = f"api/agent/v1/proposals/"
        data = [
            {
                "jobseeker_id": {
                    "id": str(self.proposal_1.jobseeker_id.id),
                    "name": "yamamoto",
                    "birth_date": "2023-05-02",
                    "gender": "female",
                    "phone_number": "11112345678",
                    "in_charge_id": {"id": str(self.user.id)},
                    "last_record_at": "2023-06-02T13:49:37+09:00",
                },
                "job_id": {
                    "id": str(self.proposal_1.job_id.id),
                    "recruiting_company_id": {
                        "id": str(self.proposal_1.job_id.recruiting_company_id.id)
                    },
                    "job_category_id": {
                        "id": str(self.proposal_1.job_id.job_category_id.id)
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
                    "trial_period": "",
                    "smoking_prevention_measure": "",
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
                "organization_id": {"id": str(self.proposal_1.organization_id.id)},
            },
            {
                "jobseeker_id": {
                    "id": str(self.proposal_2.jobseeker_id.id),
                    "name": "yamamoto",
                    "birth_date": "2023-05-02",
                    "gender": "female",
                    "phone_number": "11112345678",
                    "in_charge_id": {"id": str(self.user.id)},
                    "last_record_at": "2023-06-02T13:49:37+09:00",
                },
                "job_id": {
                    "id": str(self.proposal_2.job_id.id),
                    "recruiting_company_id": {
                        "id": str(self.proposal_2.job_id.recruiting_company_id.id)
                    },
                    "job_category_id": {
                        "id": str(self.proposal_2.job_id.job_category_id.id)
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
                    "trial_period": "",
                    "smoking_prevention_measure": "",
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
                "organization_id": {"id": str(self.proposal_2.organization_id.id)},
            },
        ]

        request = self.factory.post(
            url,
            data=data,
            format="json",
        )

        force_authenticate(request, user=self.user)
        view = ProposalBulkCreateView.as_view()
        response = view(request)

        """
        正常系 1:
        正常にデータをpostできること
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")

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

    def test_put_proposals(self):
        url = f"api/agent/v1/proposals/{self.proposal_1.id}/"
        data = [
            {
                "jobseeker_id": {
                    "id": self.proposal_1.jobseeker_id.id,
                    "name": "yamamoto",
                    "birth_date": "2023-05-02",
                    "gender": "female",
                    "phone_number": "11112345678",
                    "in_charge_id": {"id": self.user.id},
                    "last_record_at": "2023-06-02T13:49:37+09:00",
                },
                "job_id": {
                    "id": self.proposal_1.job_id.id,
                    "recruiting_company_id": {
                        "id": self.proposal_1.job_id.recruiting_company_id.id
                    },
                    "job_category_id": {
                        "id": self.proposal_1.job_id.job_category_id.id
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
                "organization_id": {"id": self.proposal_1.organization_id.id},
            }
        ]
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = ProposalBulkCreateView.as_view()
        response = view(request, pk=self.proposal_1.id)

        """
        異常系 1:
        putできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )

    def test_delete_proposal(self):
        url = f"api/agent/v1/proposals/{self.proposal_1.id}/"
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        view = ProposalBulkCreateView.as_view()
        response = view(request, pk=self.proposal_1.id)

        """
        異常系 1:
        deleteできないこと
        """
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            "HTTPステータス405が返ること.",
        )
