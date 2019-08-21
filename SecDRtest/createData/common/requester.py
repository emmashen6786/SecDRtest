# -*-coding: utf-8 -*-
import re
import time
import json
import logging

logger = logging.getLogger("django.request.autoApi")


class Requester:
    dynamicParamsValue = ""

    # 初始化requester，将脚本的http参数转换成HTTP请求需要的参数
    def __init__(self, method, url, header, path_param_template, query_param_template, form_param_template,
                 body_param_template, file_param_template, channel_id, product_code, sub_product_code,
                 market_channel_code, publice_params, **kw):
        self.method = method
        self.url = url
        self.header = header
        self.path_param_template = path_param_template
        self.query_param_template = query_param_template
        self.form_param_template = form_param_template
        self.body_param_template = body_param_template
        self.file_param_template = file_param_template
        self.channel_id = channel_id
        self.product_code = product_code
        self.sub_product_code = sub_product_code
        self.market_channel_code = market_channel_code
        self.DefaultPublicParam = publice_params

    # 准备http请求body需要的参数,#需替换
    def prepareParam(self, param, dynamicParams):  # dict,dict
        try:
            if not param:
                return
            if not dynamicParams:
                return
            for key, value in param.items():
                if isinstance(value, list):
                    for paramValue in value:
                        if isinstance(paramValue, dict):
                            for k, v in paramValue.items():
                                if isinstance(v, str) and v.startswith("$"):
                                    if dynamicParams.__contains__(k):
                                        paramValue[k] = dynamicParams.get(v.split("$")[-1], v)
                                    elif dynamicParams.__contains__(v.split("$")[-1]):
                                        paramValue[k] = dynamicParams.get(v.split("$")[-1], v)
                                    elif key == "channel_id":
                                        param[key] = self.channel_id
                                    elif key == "productCode":
                                        param[key] = self.product_code
                                    elif key == "sub_product_code":
                                        param[key] = self.sub_product_code
                                    elif key == "market_channel_code":
                                        param[key] = self.market_channel_code

                                elif isinstance(v, dict):
                                    self.prepareParam(v, dynamicParams)
                elif isinstance(value, dict):
                    self.prepareParam(value, dynamicParams)
                elif isinstance(value, str) and value.startswith("$"):
                    if dynamicParams.__contains__(key):
                        param[key] = dynamicParams.get(value.split("$")[-1], value)
                    elif key == "channel":
                        param[key] = self.channel_id
                    elif key == "productCode":
                        param[key] = self.product_code
                    elif key == "subProductCode":
                        param[key] = self.sub_product_code
                    elif key == "marketChannelCode":
                        param[key] = self.market_channel_code
                    else:
                        i = value.split("$")[-1]
                        if i == "productCode":
                            param[key] = self.product_code
            logger.info(f'prepareParam success! param:{param}')
        except Exception as e:
            error_msg = f'prepareParam error! param:{param} , dynamicParams:{dynamicParams} ,error: {e}'
            logger.error(error_msg)

    # 重新组装url，{}内参数替换，str类型
    def resetUrl(self):
        try:
            parts = re.findall(r'[{](.*?)[}]', self.url)  # 匹配url内{}里面的字段，返回list
            for part in parts:
                self.url = self.url.replace("{" + part + "}", str(self.DefaultPublicParam[part]))
            logger.info(f'resetUrl success!method:{self.method},url:{self.url}')

        except Exception as e:
            error_msg = f'resetUrl error! url:{self.url} ,error: {e}'
            logger.error(error_msg)

    def resetHeader(self):
        try:
            if self.header:
                h = eval(self.header) if isinstance(self.header, str) else self.header
                self.prepareParam(h, self.DefaultPublicParam)
                self.header = h
                logger.info(f'resetHeader success! header:{self.header}')

        except Exception as e:
            error_msg = f'resetHeader error! header:{self.header} ,error: {e}'
            logger.error(error_msg)

    def resetPath_param_template(self):
        try:
            if self.path_param_template:
                h = eval(self.path_param_template) if isinstance(self.path_param_template,
                                                                 str) else self.path_param_template
                self.prepareParam(h, self.DefaultPublicParam)
                self.path_param_template = h
                logger.info(f'resetPath_param_template success! path_param:{self.path_param_template}')
        except Exception as e:
            error_msg = f'resetPath_param_template error! path_param:{self.path_param_template} ,error: {e}'
            logger.error(error_msg)

    def resetQuery_param_template(self):
        try:
            if self.query_param_template:
                h = eval(self.query_param_template) if isinstance(self.query_param_template,
                                                                  str) else self.query_param_template
                self.prepareParam(h, self.DefaultPublicParam)
                self.query_param_template = h
                logger.info(f'resetQuery_param_template success! query param:{self.query_param_template}')
        except Exception as e:
            error_msg = f'resetQuery_param_template error! query:{self.query_param_template} ,error: {e}'
            logger.error(error_msg)

    def resetForm_param_template(self):
        try:
            if self.form_param_template:
                h = eval(self.query_param_template) if isinstance(self.query_param_template,
                                                                  str) else self.query_param_template
                self.prepareParam(h, self.DefaultPublicParam)
                self.query_param_template = h
                logger.info(f'resetForm_param_template success! form_param_template:{self.form_param_template}')
        except Exception as e:
            error_msg = f'resetForm_param_template error! form_param_template:{self.form_param_template} ,error: {e}'
            logger.error(error_msg)

    def resetBody_param_template(self):
        try:
            if self.body_param_template:
                self.body_param_template = eval(self.body_param_template) if isinstance(self.body_param_template,
                                                                                        str) else self.body_param_template

                self.prepareParam(self.body_param_template, self.DefaultPublicParam)
                if isinstance(self.body_param_template, list):
                    newbody = {}
                    for i in range(len(self.body_param_template)):
                        # self.prepareParam(i,self.dynamicParams)
                        newbody = self.body_param_template[i]
                    self.body_param_template = newbody
                    self.prepareParam(self.body_param_template, self.DefaultPublicParam)
                logger.info(f'resetBody_param_template success! body_param_template:{self.body_param_template}')
        except Exception as e:
            error_msg = f'resetBody_param_template error! body_param_template:{self.body_param_template} ,error: {e}'
            logger.error(error_msg)

    def resetSqlParams(self, sql):
        parts = re.findall(r'[{](.*?)[}]', sql)
        for part in parts:
            sql = sql.replace("{" + part + "}", str(self.DefaultPublicParam[part]))
        return sql

    def setPost(self, session):
        if not self.file_param_template:
            if self.body_param_template:
                if self.query_param_template:
                    resp = session.post(self.url, params=self.query_param_template, json=self.body_param_template,
                                        headers=self.header)
                    return resp
                else:
                    resp = session.post(self.url, json=self.body_param_template, headers=self.header)
                    return resp
            elif self.query_param_template:
                resp = session.post(self.url, params=self.query_param_template, headers=self.header)
                return resp

        elif self.file_param_template:
            filesParams = {}
            if isinstance(self.file_param_template, dict):
                for k in self.file_param_template:
                    filesParams[k] = open(self.file_param_template[k], "rb")
                if self.body_param_template:
                    if self.query_param_template:
                        resp = session.post(self.url, params=self.query_param_template, json=self.body_param_template,
                                            files=filesParams, headers=self.header)
                        return resp
                    else:
                        resp = session.post(self.url, json=self.body_param_template, files=filesParams,
                                            headers=self.header)
                        return resp
                elif self.query_param_template:
                    resp = session.post(self.url, params=self.query_param_template, files=filesParams,
                                        headers=self.header)
                    return resp
            else:
                self.file_param_template = eval(self.file_param_template)
                for k in self.file_param_template:
                    filesParams[k] = open(self.file_param_template[k], "rb")
                if self.body_param_template:
                    if self.query_param_template:
                        resp = session.post(self.url, params=self.query_param_template, json=self.body_param_template,
                                            files=filesParams, headers=self.header)
                        return resp
                    else:
                        resp = session.post(self.url, json=self.body_param_template, files=filesParams,
                                            headers=self.header)
                        return resp
                elif self.query_param_template:
                    resp = session.post(self.url, params=self.query_param_template, files=filesParams,
                                        headers=self.header)
                    return resp

    def setGet(self, session):
        if not self.query_param_template:
            resp = session.get(self.url, params=self.body_param_template, headers=self.header)
            return resp
        elif self.query_param_template:
            resp = session.get(self.url, params=self.query_param_template, headers=self.header)
            return resp

    def setPut(self, session):
        if self.body_param_template:
            if self.query_param_template != '':
                resp = session.put(self.url, params=self.query_param_template, json=self.body_param_template,
                                   headers=self.header)
                return resp
            else:
                resp = session.put(self.url, json=self.body_param_template, headers=self.header)
                return resp
        elif self.query_param_template:
            resp = session.put(self.url, params=self.query_param_template, headers=self.header)
            return resp

    # 获取返回报文里需要保留的字段
    def getRealDynamicParam(self, data, dynamicParamsKey):  # dict,str
        if dynamicParamsKey in data.keys():
            self.dynamicParamsValue = data[dynamicParamsKey]
            return self.dynamicParamsValue
        for key in data.keys():
            if isinstance(data[key], list):
                for dataValue in data[key]:
                    if isinstance(dataValue, dict):
                        for k, v in dataValue.items():
                            if dynamicParamsKey == k:
                                self.dynamicParamsValue = v
                                return self.dynamicParamsValue
                            elif isinstance(v, dict):
                                self.dynamicParamsValue = self.getRealDynamicParam(v, dynamicParamsKey)
                                if self.dynamicParamsValue:
                                    return self.dynamicParamsValue
            elif isinstance(data[key], dict):
                self.dynamicParamsValue = self.getRealDynamicParam(data[key], dynamicParamsKey)
                if self.dynamicParamsValue:
                    return self.dynamicParamsValue
