from django.urls import reverse

from rest_framework import status

from core.common import CLUSTER_TYPES, PRP_ROLE_TYPES
from core.models import Workspace, ResponsePlan, Location
from core.factories import ClusterPRPRoleFactory
from core.tests.base import BaseAPITestCase


class TestWorkspaceListAPIView(BaseAPITestCase):

    def test_list_api(self):
        url = reverse('workspace')
        response = self.client.get(url, format='json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            len(response.data),
            Workspace.objects.prefetch_related('locations').filter(
                locations__isnull=False).distinct().count()
        )


class TestLocationListAPIView(BaseAPITestCase):

    def test_list_api(self):
        response_plan_id = ResponsePlan.objects.first().id
        url = reverse(
            'location', kwargs={
                'response_plan_id': response_plan_id})
        response = self.client.get(url, format='json')

        result = ResponsePlan.objects.filter(id=response_plan_id).values_list(
            'clusters__cluster_objectives__reportables__locations',
            'clusters__cluster_objectives__cluster_activities__reportables__locations',
            'clusters__partner_projects__reportables__locations',
            'clusters__partner_projects__partner_activities__reportables__locations',
        ).distinct()
        pks = []
        [pks.extend(filter(lambda x: x is not None, part)) for part in result]
        expected = Location.objects.filter(pk__in=pks).count()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), expected)


class TestResponsePlanAPIView(BaseAPITestCase):

    def setUp(self):
        super(TestResponsePlanAPIView, self).setUp()
        self.workspace = Workspace.objects.first()

        ClusterPRPRoleFactory(
            user=self.user,
            role=PRP_ROLE_TYPES.imo_cluster,
        )

    def test_response_plan(self):
        rp_data = {
            'title': 'Test Response Plan',
            'plan_type': 'HRP',
            'start': '2013-01-01',
            'end': '2018-01-01',
            'clusters': [
                CLUSTER_TYPES.cccm,
                CLUSTER_TYPES.nutrition,
            ],
        }

        url = reverse("response-plan-create", kwargs={'workspace_id': self.workspace.id})
        response = self.client.post(url, data=rp_data, format='json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED, msg=response.content)

    def test_end_lt_start(self):
        rp_data = {
            'title': 'Test Response Plan',
            'plan_type': 'HRP',
            'start': '2018-01-01',
            'end': '2013-01-01',
            'clusters': [
                CLUSTER_TYPES.cccm,
                CLUSTER_TYPES.nutrition,
            ],
        }

        url = reverse("response-plan-create", kwargs={'workspace_id': self.workspace.id})
        response = self.client.post(url, data=rp_data, format='json')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
