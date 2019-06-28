from django.test import TestCase
from createData.models import RequestConfig


class FruitTestCase(TestCase):
    # 初始化代码
    def setUp(self):
        RequestConfig.objects.create(name="apple", description="hand", request_method="Get",
                                     request_url="http://baidu.com", request_header="")

    def test_RequestConfig(self):
        request = RequestConfig.objects.get(id=1)
        self.assertEqual(request.name, 'apple')





