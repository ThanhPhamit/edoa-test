import copy
import uuid
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from api.tests import factories

from api.views import ProposalBulkUpdateView
from api.serializers import ProposalSerializer


class ProposalBulkUpdateTests(APITestCase):
    url = f"api/agent/v1/proposals/bulk_update/"

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
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = ProposalBulkUpdateView.as_view()
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

    def test_post_proposals(self):
        request = self.factory.post(
            self.url,
            data=[],
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = ProposalBulkUpdateView.as_view()
        response = view(request)

        """
        異常系 1:
        postできないこと
        """
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, "HTTPステータス405が返ること.")

    def test_put_proposals(self):
        request = self.factory.put(
            self.url,
            data=[],
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = ProposalBulkUpdateView.as_view()
        response = view(request)

        """
        異常系 1:
        putできないこと
        """
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, "HTTPステータス405が返ること.")

    def test_delete_proposal(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        view = ProposalBulkUpdateView.as_view()
        response = view(request)

        """
        異常系 1:
        deleteできないこと
        """
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, "HTTPステータス405が返ること.")

    def test_patch_proposal(self):
        request = self.factory.patch(
            self.url,
            data=[{"id": self.proposal_1.id, "position": "TEST00"}, {"id": self.proposal_2.id, "position": "TEST01"}],
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = ProposalBulkUpdateView.as_view()
        response = view(request)

        """
        正常系 1:
        正常にpatchできること
        """
        self.assertEqual(response.status_code, status.HTTP_200_OK, "HTTPステータス200が返ること")
        self.assertEqual(len(response.data), 2, "更新件数が2件であること")
        for i in range(0, 1):
            self.assertEqual(response.data[i]["position"], f"TEST0{i}", "更新が反映されていること")
            for key in ProposalSerializer.Meta.fields:
                self.assertIn(key, response.data[i].keys(),"Proposalが返ること")

        """
        異常系 1:
        認証されていないユーザーがpatchをリクエストした場合、エラーが返ること
        """
        request_unauthorize = self.factory.patch(
            self.url,
            data=[{"id": self.proposal_1.id, "position": "MUST NOT UPDATE"}, {"id": self.proposal_2.id, "position": "MUST NOT UPDATE"}],
            format="json",
        )
        reponse_unauthorize = view(request_unauthorize)

        self.assertEqual(reponse_unauthorize.status_code, status.HTTP_401_UNAUTHORIZED, "HTTPステータス401が返ること.")

        """
        異常系 2:
        リスエストボディのProposalにIDがない要素がある場合、エラーが返り、全て更新されないこと
        """
        request_no_id = self.factory.patch(
            self.url,
            data=[{"id": self.proposal_1.id, "position": "MUST NOT UPDATE"}, {"position": "MUST NOT UPDATE"}],
            format="json",
        )
        force_authenticate(request_no_id, user=self.user)
        reponse_no_id = view(request_no_id)
        
        self.assertEqual(reponse_no_id.status_code, status.HTTP_400_BAD_REQUEST, "HTTPステータス400が返ること.")
        self.proposal_1.refresh_from_db()
        self.proposal_2.refresh_from_db()
        self.assertEqual(self.proposal_1.position, "TEST00", "更新されていないこと")
        self.assertEqual(self.proposal_2.position, "TEST01", "更新されていないこと")

        """
        異常系 3:
        リスエストボディのProposalのIDが存在しない場合、エラーが返り、全て更新されないこと
        """
        request_no_id = self.factory.patch(
            self.url,
            data=[{"id": self.proposal_1.id, "position": "MUST NOT UPDATE"}, {"id": str(uuid.uuid4()), "position": "MUST NOT UPDATE"}],
            format="json",
        )
        force_authenticate(request_no_id, user=self.user)
        reponse_no_id = view(request_no_id)
        
        self.assertEqual(reponse_no_id.status_code, status.HTTP_404_NOT_FOUND, "HTTPステータス404が返ること.")
        self.proposal_1.refresh_from_db()
        self.proposal_2.refresh_from_db()
        self.assertEqual(self.proposal_1.position, "TEST00", "更新されていないこと")
        self.assertEqual(self.proposal_2.position, "TEST01", "更新されていないこと")