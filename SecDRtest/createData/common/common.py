from createData import models
import time


def record_results(_id, method, url, header, path_param_template, query_param_template, form_param_template,
                   body_param_template, file_param_template, result, status_code, response_data, updated_time):
    """
    记录手动测试结果
    :param _id: automationCaseApi
    :param url:  请求地址
    :param method:  请求方式
    :param header: 请求头
    :param path_param_template: 路径请求参数
    :param query_param_template: ？后请求参数
    :param form_param_template: 表单请求参数
    :param body_param_template: body请求参数
    :param file_param_template: 文件请求参数
    :param result:  成功/失败
    :param status_code: HTTP状态
    :param response_data:  返回结果
    :return:
    """
    rt = models.AutomationTestResult.objects.filter(automationCaseApi=_id)
    if rt:
        rt.update(request_method=method, request_url=url, request_header=header,
                  path_param_template=path_param_template, query_param_template=query_param_template,
                  form_param_template=form_param_template, body_param_template=body_param_template,
                  file_param_template=file_param_template, result=result, statusCode=status_code,
                  responseData=response_data, updated_time=updated_time)
    else:
        result_ = models.AutomationTestResult(automationCaseApi=models.RequestConfig.objects.get(id=_id),
                                              request_method=method, request_url=url, request_header=header,
                                              path_param_template=path_param_template,
                                              query_param_template=query_param_template,
                                              form_param_template=form_param_template,
                                              body_param_template=body_param_template,
                                              file_param_template=file_param_template,
                                              result=result, statusCode=status_code, responseData=response_data)
        result_.save()
