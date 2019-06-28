from django.shortcuts import render
from . import models
from . import serializers
from createData.common.helper import CommonModelViewSet


class RequestViewSet(CommonModelViewSet):
    """
    retrieve:
        查询api请求.
    list:
        查询所有的api请求.
    create:
        新建api请求.
    destroy:
        删除api请求.
    update:
        更新api请求.
    partial_update:
        更新api请求.
    """
    queryset = models.RequestConfig.objects.all()
    serializer_class = serializers.RequestConfigSerializer


class ResponseViewSet(CommonModelViewSet):
    """
    retrieve:
        查询api返回配置.
    list:
        查询所有的api返回配置.
    create:
        新建api返回配置.
    destroy:
        删除api返回配置.
    update:
        更新api返回配置.
    partial_update:
        更新api返回配置.
    """
    queryset = models.ResponseConfig.objects.all()
    serializer_class = serializers.ResponseConfigSerializer


class DefaultPublicParamViewSet(CommonModelViewSet):
    """
    retrieve:
        查询默认参数配置.
    list:
        查询所有的默认参数配置.
    create:
        新建默认参数配置.
    destroy:
        删除默认参数配置.
    update:
        更新默认参数配置.
    partial_update:
        更新默认参数配置.
    """
    queryset = models.DefaultPublicParam.objects.all()
    serializer_class = serializers.DefaultPublicParamSerializer


class RequestRelationViewSet(CommonModelViewSet):
    """
    retrieve:
        查询某个关联api.
    list:
        查询所有关联api.
    create:
        新建关联api.
    destroy:
        删除某个关联api.
    update:
        更新某个关联api.
    partial_update:
        更新某个关联api.
    """
    queryset = models.RequestRelation.objects.all()
    serializer_class = serializers.RequestRelationSerializer


class RequestGroupViewSet(CommonModelViewSet):
    """
    retrieve:
        查询某个请求组详细信息.
    list:
        查询所有请求组.
    create:
        新建请求组并同时创建关联请求.
    destroy:
        删除某个请求组及关联请求.
    update:
        更新某个请求组及关联请求.
    partial_update:
        更新某个请求组及关联请求.
    """
    queryset = models.RequestGroup.objects.all()
    serializer_class = serializers.RequestGroupSerializer
    retrieve_serializer_class = serializers.RequestGroupRetrieveSerializer
    update_serializer_class = serializers.RequestGroupUpdateSerializer
    create_serializer_class = serializers.RequestGroupCreateSerializer

    def perform_create(self, create_serializer):
        create_serializer.save()
        requestGroup = create_serializer.instance
        requestRelation = models.RequestRelation.objects.filter(request_group=requestGroup)

        if 'relationRequests' in self.request.data:
            for request_id in self.request.data['relationRequests']:
                if 'name' in request_id and 'description' in request_id and 'request_id' in request_id:
                    rer = requestRelation.get(request_id_id=request_id['request_id'])
                    rer.name = request_id['name']
                    rer.description = request_id['description']
                    rer.save()

    def perform_update(self, update_serializer):
        update_serializer.save()
        requestGroup = update_serializer.instance
        requestRelation = models.RequestRelation.objects.filter(request_group=requestGroup)

        if 'relationRequests' in self.request.data:
            for request_id in self.request.data['relationRequests']:
                if 'name' in request_id and 'description' in request_id and 'id' in request_id:
                    rer = requestRelation.get(request_id_id=request_id['id'])
                    rer.name = request_id['name']
                    rer.description = request_id['description']
                    rer.save()


class RequestGroupEasyViewSet(CommonModelViewSet):
    queryset = models.RequestGroup.objects.all()
    serializer_class = serializers.RequestGroupEasySerializer


class AutomationTestResultViewSet(CommonModelViewSet):
    """
    retrieve:
        查询某个api测试结果.
    list:
        查询所有api测试结果.
    create:
        新建api测试结果.
    destroy:
        删除某个api测试结果.
    update:
        更新某个api测试结果.
    partial_update:
        更新某个api测试结果.
    """
    queryset = models.AutomationTestResult.objects.all()
    serializer_class = serializers.AutomationTestResultSerializer


class ResultRelationViewSet(CommonModelViewSet):
    """
    retrieve:
        查询某个关联api结果.
    list:
        查询所有关联api结果.
    create:
        新建关联api结果.
    destroy:
        删除某个关联api结果.
    update:
        更新某个关联api结果.
    partial_update:
        更新某个关联api结果.
    """
    queryset = models.ResultRelation.objects.all()
    serializer_class = serializers.ResultRelationSerializer


class ResultGroupViewSet(CommonModelViewSet):
    """
    retrieve:
        查询某个结果组详细信息.
    list:
        查询所有结果组.
    create:
        新建结果组并同时创建关联请求结果.
    destroy:
        删除某个结果组及关联请求结果.
    update:
        更新某个结果组及关联请求结果.
    partial_update:
        更新某个结果组及关联请求结果.
    """
    queryset = models.ResultGroup.objects.all()
    serializer_class = serializers.ResultGroupSerializer
    retrieve_serializer_class = serializers.ResultGroupRetrieveSerializer
    update_serializer_class = serializers.ResultGroupUpdateSerializer
    create_serializer_class = serializers.ResultGroupCreateSerializer

    def perform_create(self, create_serializer):
        create_serializer.save()
        resultGroup = create_serializer.instance
        resultRelation = models.ResultRelation.objects.filter(result_group=resultGroup)

        if 'relationRequests' in self.request.data:
            for request_id in self.request.data['relationRequests']:
                if 'name' in request_id and 'description' in request_id and 'request_id' in request_id:
                    rer = resultRelation.get(request_id_id=request_id['request_id'])
                    rer.name = request_id['name']
                    rer.description = request_id['description']
                    rer.save()

    def perform_update(self, update_serializer):
        update_serializer.save()
        resultGroup = update_serializer.instance
        resultRelation = models.ResultRelation.objects.filter(result_group=resultGroup)

        if 'relationRequests' in self.request.data:
            for request_id in self.request.data['relationRequests']:
                if 'name' in request_id and 'automationCaseApi' in request_id:
                    rer = resultRelation.get(request_id_id=request_id['automationCaseApi'])
                    rer.name = request_id['name']
                    rer.save()


class AutomationReportSendConfigViewSet(CommonModelViewSet):
    """
    retrieve:
        查询某个报告配置.
    list:
        查询所有报告配置.
    create:
        新建报告配置.
    destroy:
        删除某个报告配置.
    update:
        更新某个报告配置.
    partial_update:
        更新某个报告配置.
    """
    queryset = models.AutomationReportSendConfig.objects.all()
    serializer_class = serializers.AutomationReportSendConfigSerializer
