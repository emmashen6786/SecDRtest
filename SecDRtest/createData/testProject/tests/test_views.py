from django.test import TestCase

# Create your tests here.

from createData.models import RequestConfig
from django.urls import reverse


class RequestConfigViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_RequestConfig = 13
        for num in range(number_of_RequestConfig):
            RequestConfig.objects.create(name='Christian %s' % num, request_url='request_url %s' % num, )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/api/v1/requestconfig/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get('/api/v1/requestconfig/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/api/v1/requestconfig/')
        self.assertEqual(resp.status_code, 200)

