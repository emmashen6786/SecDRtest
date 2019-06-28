from createData import models
from createData import serializers
import json
from createData.common.requester import Requester
from createData.common.common import record_results
import time
import requests
from requests import ReadTimeout

import re
import logging

logger = logging.getLogger("django.request.autoApi")


class AutoApi(object):
    def __init__(self, defult_param):
        self.session = requests.session()
        self.defult_param = defult_param

    def run(self, data, responseConfig_data):
        """
        执行接口测试
        :param data: 请求数据
        :param defult_param: 默认公共参数数据
        :param responseConfig_data: 期待结果数据
        :return:
        """
        method = data["request_method"]
        url = data["request_url"]
        header = data["request_header"]
        path_param_template = data["path_param_template"]
        query_param_template = data["query_param_template"]
        form_param_template = data["form_param_template"]
        body_param_template = data["body_param_template"]
        file_param_template = data["file_param_template"]
        channel_id = self.defult_param["channel_id"]
        product_code = self.defult_param["product_code"]
        sub_product_code = self.defult_param["sub_product_code"]
        market_channel_code = self.defult_param["market_channel_code"]
        publice_params = eval(self.defult_param["publice_params"]) if isinstance(self.defult_param["publice_params"],
                                                                                 str) else self.defult_param[
            "publice_params"]

        response_data = {}

        requester = Requester(method, url, header, path_param_template, query_param_template, form_param_template,
                              body_param_template, file_param_template, channel_id, product_code, sub_product_code,
                              market_channel_code, publice_params)
        requester.resetUrl()
        requester.resetHeader()
        requester.resetBody_param_template()
        requester.resetQuery_param_template()
        try:
            if method == "POST":
                resp = requester.setPost(self.session)
            elif method == "PUT":
                resp = requester.setPut(self.session)
            elif method == "GET":
                resp = requester.setGet(self.session)
            else:
                response_data = {"result": "ERROR"}
                return response_data
        except ReadTimeout:
            response_data = {"result": "TimeOut"}
            record_results(_id=data["id"],
                           method=method, url=url, header=header,
                           path_param_template=path_param_template,
                           query_param_template=query_param_template,
                           form_param_template=form_param_template,
                           body_param_template=body_param_template,
                           file_param_template=file_param_template,
                           result="TimeOut",
                           status_code="",
                           response_data="",
                           updated_time=time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime()))
            return response_data

        try:
            if resp.status_code in [200, 201, 204]:
                logger.info(f'request success!')
                if resp.text != '':
                    content = json.loads(resp.text)
                    try:
                        if responseConfig_data["dependent_param_list"]:
                            response_dependent_param = eval(responseConfig_data["dependent_param_list"])
                            if isinstance(response_dependent_param, dict):
                                for k, v in response_dependent_param.items():
                                    if "paramList" == k:
                                        if isinstance(v, list):
                                            for f in v:
                                                if isinstance(f, dict):
                                                    responseRetainKey = f["responseRetainKey"]
                                                    dynamicParamsKey = f["dynamicParamsKey"]
                                                    if isinstance(content, dict):
                                                        dynamicParamsValue = requester.getRealDynamicParam(
                                                            content, responseRetainKey)
                                                        publice_params[dynamicParamsKey] = dynamicParamsValue
                                                        self.defult_param["publice_params"] = publice_params
                                                    elif isinstance(content, list):
                                                        dynamicParamsValue = requester.getRealDynamicParam(
                                                            content[-1], responseRetainKey)
                                                        publice_params[dynamicParamsKey] = dynamicParamsValue
                                                        self.defult_param["publice_params"] = publice_params
                            logger.info(
                                f'update defult_param success! response_dependent_param is {response_dependent_param}')

                    except Exception as e:
                        error_msg = f'update defult_param error!error: {e}'
                        logger.error(error_msg)
                    try:
                        if responseConfig_data["expect_response"]:
                            if isinstance(responseConfig_data["expect_response"], str):
                                for k, v in eval(responseConfig_data["expect_response"]).items():
                                    if k in content.keys() and v == content[k]:
                                        response_data = {"result": "SUCCESS", "content": content}
                                        logger.info(f'expect_response is right!')
                                        record_results(_id=data["id"],
                                                       method=method, url=url, header=header,
                                                       path_param_template=path_param_template,
                                                       query_param_template=query_param_template,
                                                       form_param_template=form_param_template,
                                                       body_param_template=body_param_template,
                                                       file_param_template=file_param_template,
                                                       result="success!has expect_response",
                                                       status_code=resp.status_code,
                                                       response_data=json.dumps(resp.text),
                                                       updated_time=time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                  time.localtime()))
                                    else:
                                        response_data = {"result": "FAIL", "content": content}
                                        logger.error(f'expect_response is fail!,{response_data}')
                                        record_results(_id=data["id"],
                                                       method=method, url=url, header=header,
                                                       path_param_template=path_param_template,
                                                       query_param_template=query_param_template,
                                                       form_param_template=form_param_template,
                                                       body_param_template=body_param_template,
                                                       file_param_template=file_param_template,
                                                       result="fail!content has no right expect_response",
                                                       status_code=resp.status_code,
                                                       response_data=json.dumps(resp.text),
                                                       updated_time=time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                  time.localtime()))
                        else:
                            response_data = {"result": "SUCCESS", "content": content}
                            logger.info(f'success!has no expect_response')
                            record_results(_id=data["id"],
                                           method=method, url=url, header=header,
                                           path_param_template=path_param_template,
                                           query_param_template=query_param_template,
                                           form_param_template=form_param_template,
                                           body_param_template=body_param_template,
                                           file_param_template=file_param_template,
                                           result="success!has no expect_response",
                                           status_code=resp.status_code,
                                           response_data=json.dumps(resp.text),
                                           updated_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    except Exception as e:
                        error_msg = f'expect_response error! error: {e}'
                        logger.error(error_msg)

                else:
                    response_data = {"result": "SUCCESS", "content": resp.text}
                    logger.info(f'success!has no response')
                    record_results(_id=data["id"],
                                   method=method, url=url, header=header,
                                   path_param_template=path_param_template,
                                   query_param_template=query_param_template,
                                   form_param_template=form_param_template,
                                   body_param_template=body_param_template,
                                   file_param_template=file_param_template,
                                   result="success!has no response",
                                   status_code=resp.status_code,
                                   response_data=json.dumps(resp.text),
                                   updated_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            else:
                response_data = {"result": "FAIL", "content": resp.text}
                logger.error(f'request is fail!,content:{resp.text}')
                record_results(_id=data["id"],
                               method=method, url=url, header=header,
                               path_param_template=path_param_template,
                               query_param_template=query_param_template,
                               form_param_template=form_param_template,
                               body_param_template=body_param_template,
                               file_param_template=file_param_template,
                               result="fail",
                               status_code=resp.status_code,
                               response_data=json.dumps(resp.text),
                               updated_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            return response_data
        except Exception:
            error_msg = f'request error!error: {resp.text}'
            logger.error(error_msg)
