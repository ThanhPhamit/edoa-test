from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from datetime import datetime
from api.tests import factories

from api.views import JobseekerProposalViewSet


class JobseekerProposalTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = factories.UserFactory()
        self.proposal_1 = factories.ProposalFactory(
            organization_id=self.user.organization_id,
        )
        self.proposal_2 = factories.ProposalFactory()

    def test_get_proposals(self):
        url = f"api/jobseeker/v1/proposals/?jobseeker_id={self.proposal_1.jobseeker_id.id}"
        request = self.factory.get(url)
        view = JobseekerProposalViewSet.as_view({"get": "list"})
        response = view(request)
        data = response.data

        """
        正常系 1:
        正常にデータをgetできること
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(len(data), 1, "1件取得できること.")
        self.assertEqual(
            data[0]["job_id"]["id"],
            str(self.proposal_1.job_id.id),
            "job_id id カラムの検証.",
        )
        self.assertEqual(
            data[0]["intention"],
            self.proposal_1.intention,
            "intention カラムの検証.",
        )
        self.assertEqual(
            data[0]["is_favorite"],
            self.proposal_1.is_favorite,
            "is_favorite カラムの検証.",
        )
        self.assertEqual(
            data[0]["comment"],
            self.proposal_1.comment,
            "comment カラムの検証.",
        )
        self.assertEqual(
            data[0]["is_public"],
            self.proposal_1.is_public,
            "is_public カラムの検証.",
        )
        self.assertEqual(
            data[0]["position"],
            self.proposal_1.position,
            "position カラムの検証.",
        )
        self.assertEqual(
            data[0]["salary"],
            self.proposal_1.salary,
            "salary カラムの検証.",
        )
        self.assertEqual(
            data[0]["summary"],
            self.proposal_1.summary,
            "summary カラムの検証.",
        )
        self.assertEqual(
            data[0]["min_qualifications"],
            self.proposal_1.min_qualifications,
            "min_qualifications カラムの検証.",
        )
        self.assertEqual(
            data[0]["pfd_qualifications"],
            self.proposal_1.pfd_qualifications,
            "pfd_qualifications カラムの検証.",
        )
        self.assertEqual(
            data[0]["ideal_profile"],
            self.proposal_1.ideal_profile,
            "ideal_profile カラムの検証.",
        )
        self.assertEqual(
            data[0]["is_appeal_layer"],
            self.proposal_1.is_appeal_layer,
            "is_appeal_layer カラムの検証.",
        )
        self.assertEqual(
            data[0]["is_appeal_remote"],
            self.proposal_1.is_appeal_remote,
            "is_appeal_remote カラムの検証.",
        )

        """
        異常系 1:
        項目を読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data[0]["jobseeker_id"]

    def test_get_proposal(self):
        url = f"api/jobseeker/v1/proposals/{self.proposal_1.id}/?jobseeker_id={self.proposal_1.jobseeker_id.id}"
        request = self.factory.get(url)
        view = JobseekerProposalViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.proposal_1.id)
        data = response.data

        """
        正常系 1:
        正常にデータをgetできること
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            data["job_id"]["id"],
            str(self.proposal_1.job_id.id),
            "job_id id カラムの検証.",
        )
        self.assertEqual(
            data["intention"],
            self.proposal_1.intention,
            "intention カラムの検証.",
        )
        self.assertEqual(
            data["is_favorite"],
            self.proposal_1.is_favorite,
            "is_favorite カラムの検証.",
        )
        self.assertEqual(
            data["comment"],
            self.proposal_1.comment,
            "comment カラムの検証.",
        )
        self.assertEqual(
            data["is_public"],
            self.proposal_1.is_public,
            "is_public カラムの検証.",
        )
        self.assertEqual(
            data["position"],
            self.proposal_1.position,
            "position カラムの検証.",
        )
        self.assertEqual(
            data["salary"],
            self.proposal_1.salary,
            "salary カラムの検証.",
        )
        self.assertEqual(
            data["summary"],
            self.proposal_1.summary,
            "summary カラムの検証.",
        )
        self.assertEqual(
            data["min_qualifications"],
            self.proposal_1.min_qualifications,
            "min_qualifications カラムの検証.",
        )
        self.assertEqual(
            data["pfd_qualifications"],
            self.proposal_1.pfd_qualifications,
            "pfd_qualifications カラムの検証.",
        )
        self.assertEqual(
            data["ideal_profile"],
            self.proposal_1.ideal_profile,
            "ideal_profile カラムの検証.",
        )
        self.assertEqual(
            data["is_appeal_layer"],
            self.proposal_1.is_appeal_layer,
            "is_appeal_layer カラムの検証.",
        )
        self.assertEqual(
            data["is_appeal_remote"],
            self.proposal_1.is_appeal_remote,
            "is_appeal_remote カラムの検証.",
        )

        """
        異常系 1:
        項目を読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            data["jobseeker_id"]

    def test_post_proposals(self):
        url = "api/jobseeker/v1/proposals/"
        data = {
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
        }
        request = self.factory.post(
            url,
            data=data,
            format="json",
        )

        view = JobseekerProposalViewSet.as_view({"post": "create"})

        """
        異常系 1:
        postできないこと
        """
        with self.assertRaises(AttributeError) as raises:
            view(request)

    def test_put_proposals(self):
        url = f"api/jobseeker/v1/proposals/{self.proposal_1.id}/?jobseeker_id={self.proposal_1.jobseeker_id.id}"
        data = {
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
                "job_category_id": {"id": self.proposal_1.job_id.job_category_id.id},
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
        request = self.factory.put(
            url,
            data=data,
            format="json",
        )

        view = JobseekerProposalViewSet.as_view({"put": "update"})
        response = view(request, pk=self.proposal_1.id)

        """
        正常系 1:
        正常にデータをputできること
        """
        url_updated_data = f"api/agent/v1/proposals/{self.proposal_1.id}/?jobseeker_id={self.proposal_1.jobseeker_id.id}"
        request_updated_data = self.factory.get(url_updated_data)
        view_get = JobseekerProposalViewSet.as_view({"get": "retrieve"})
        response_updated_data = view_get(request_updated_data, pk=self.proposal_1.id)
        updated_data = response_updated_data.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること.")
        self.assertEqual(
            updated_data["job_id"]["id"],
            str(data["job_id"]["id"]),
            "job_id id カラムの検証.",
        )
        self.assertEqual(
            updated_data["intention"],
            data["intention"],
            "intention カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_favorite"],
            data["is_favorite"],
            "is_favorite カラムの検証.",
        )
        self.assertEqual(
            updated_data["comment"],
            self.proposal_1.comment,
            "comment カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_public"],
            self.proposal_1.is_public,
            "is_public カラムの検証.",
        )
        self.assertEqual(
            updated_data["position"],
            self.proposal_1.position,
            "position カラムの検証.",
        )
        self.assertEqual(
            updated_data["salary"],
            self.proposal_1.salary,
            "salary カラムの検証.",
        )
        self.assertEqual(
            updated_data["summary"],
            self.proposal_1.summary,
            "summary カラムの検証.",
        )
        self.assertEqual(
            updated_data["min_qualifications"],
            self.proposal_1.min_qualifications,
            "min_qualifications カラムの検証.",
        )
        self.assertEqual(
            updated_data["pfd_qualifications"],
            self.proposal_1.pfd_qualifications,
            "pfd_qualifications カラムの検証.",
        )
        self.assertEqual(
            updated_data["ideal_profile"],
            self.proposal_1.ideal_profile,
            "ideal_profile カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_appeal_layer"],
            self.proposal_1.is_appeal_layer,
            "is_appeal_layer カラムの検証.",
        )
        self.assertEqual(
            updated_data["is_appeal_remote"],
            self.proposal_1.is_appeal_remote,
            "is_appeal_remote カラムの検証.",
        )

        """
        異常系 1:
        項目を読み出せないこと
        """
        with self.assertRaises(KeyError) as raises:
            updated_data["jobseeker_id"]

    def test_delete_proposal(self):
        url = f"api/jobseeker/v1/proposals/{self.proposal_1.id}/"
        request = self.factory.delete(url)
        view = JobseekerProposalViewSet.as_view({"delete": "destroy"})

        """
        異常系 1:
        deleteできないこと
        """
        with self.assertRaises(AttributeError) as raises:
            view(request, pk=self.proposal_1.id)
