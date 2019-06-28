from django.test import TestCase
from createData.models import RequestConfig


class TestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        RequestConfig.objects.create(name='Big', request_method='GET', request_url='http://baidu.com')

    def test_name_label(self):
        name = RequestConfig.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label, '名称')

    def test_request_url(self):
        url = RequestConfig.objects.get(id=1)
        field_label = url._meta.get_field('request_url').verbose_name
        self.assertEquals(field_label, '接口地址')

    def test_get_absolute_url(self):
        author = RequestConfig.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/api/v1/requestconfig/')


