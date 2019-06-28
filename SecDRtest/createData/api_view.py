from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from . import models
from django.core.exceptions import ObjectDoesNotExist
from . import serializers
from createData.common.JsonResponse import JsonResponse
from createData.common.autoApi import AutoApi
from createData.common.sendEmail import sendEmail
import logging
import time

logger = logging.getLogger("django.request.autoApi")


class StartAutoApiViewSet(APIView):
    serializer_class = serializers.StartAutoApiSerializer
    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验request_group, id类型为int
            if not data["request_group"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["request_group"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        执行测试用例
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        singleResult = []
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        _pass = 0
        fail = 0
        error = 0
        time_out = 0
        if result:
            return result
        try:
            pro_data = models.RequestRelation.objects.filter(request_group_id=data["request_group"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="关联的请求不存在！")
        try:
            public_data = models.DefaultPublicParam.objects.get(market_channel_code=data["market_channel_code"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="关联的默认参数不存在！")

        pro_data_total = serializers.RequestRelationSerializer(pro_data, many=True).data
        public_data = serializers.DefaultPublicParamSerializer(public_data).data

        api = AutoApi(public_data)
        if len(pro_data_total):
            for i in range(len(pro_data_total)):
                try:
                    pro_data = pro_data_total[i]
                    request_data = models.RequestConfig.objects.get(id=pro_data["request_id"])
                    request_data = serializers.RequestConfigSerializer(request_data).data

                    response_config = models.ResponseConfig.objects.get(related_reqid=pro_data["request_id"])
                    response_data = serializers.ResponseConfigSerializer(response_config).data

                    # try:
                    #     test_result = models.AutomationTestResult.objects.get(
                    #         automationCaseApi_id=pro_data["request_id"])
                    #     if test_result:
                    #         models.AutomationTestResult.objects.filter(id=pro_data["request_id"]).delete()
                    # except Exception:
                    #     pass

                    try:

                        response_result = api.run(data=request_data, responseConfig_data=response_data)
                        if response_result["result"] == 'SUCCESS':
                            _pass = _pass + 1
                        elif response_result["result"] == 'FAIL':
                            fail = fail + 1
                        elif response_result["result"] == 'ERROR':
                            error = error + 1
                        elif response_result["result"] == 'TimeOut':
                            time_out = time_out + 1
                        singleResult.append(response_result)

                    except Exception as e:
                        error_msg = f'requestGroup {data["request_group"]} has something wrong,{e}'
                        logger.warning(error_msg)
                        return JsonResponse(code="999998", msg="失败！")

                except Exception as e:
                    error_msg = f'requestGroup {data["request_group"]} has something wrong, {e}'
                    logger.warning(error_msg)
                    return JsonResponse(code="999998", msg="失败！")

            total = _pass + fail + error + time_out
            singleResult = {
                'msg': "成功！",
                '接口总数': total,
                'result': singleResult
            }
            email_data = "Hi, all:\n    测试时间： %s\n" \
                         "    总执行测试接口数： %s:\n" \
                         "    成功： %s,  失败： %s, 执行错误： %s, 超时： %s\n" \
                         "    详情查看地址：http://127.0.0.1:8000/api/v1/result_group/%s\n" % (
                             start_time, total, _pass, fail, error, time_out, data["result_group"])

            if sendEmail(data["result_group"], email_data):
                print("邮件发送成功")
            else:
                print("邮件发送失败")

            return JsonResponse(data={
                "result": singleResult
            }, code="999999", msg="成功！")
