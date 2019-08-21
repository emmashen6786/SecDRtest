from rest_framework import serializers
from .models import RequestConfig, ResponseConfig, DefaultPublicParam, RequestGroup, RequestRelation, \
    AutomationTestResult, ResultRelation, ResultGroup, AutomationReportSendConfig

from . import models
from rest_framework import serializers


class RequestConfigSerializer(serializers.ModelSerializer):
    request_header = serializers.JSONField()
    path_param_template = serializers.JSONField()
    query_param_template = serializers.JSONField()
    form_param_template = serializers.JSONField()
    body_param_template = serializers.JSONField()
    file_param_template = serializers.JSONField()

    class Meta:
        model = RequestConfig
        fields = ('id', 'name', 'description', 'created_time', 'request_method', 'request_url', 'request_header',
                  'path_param_template', 'query_param_template', 'form_param_template', 'body_param_template',
                  'file_param_template')


class ResponseConfigSerializer(serializers.ModelSerializer):
    dependent_param_list = serializers.JSONField()
    expect_response = serializers.JSONField()

    class Meta:
        model = ResponseConfig
        fields = (
            'id', 'name', 'description', 'created_time', 'related_reqid', 'dependent_param_list', 'expect_response')


class DefaultPublicParamSerializer(serializers.ModelSerializer):
    publice_params = serializers.JSONField()
    product_code=serializers.JSONField()

    class Meta:
        model = DefaultPublicParam
        fields = (
            'id', 'name', 'description', 'created_time', 'channel_id', 'product_code', 'sub_product_code',
            'market_channel_code', 'publice_params'
        )


class RequestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestGroup
        fields = ('id', 'name')


class RequestRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestRelation
        fields = ('name', 'request_id')


class RequestGroupEasySerializer(serializers.ModelSerializer):
    RequestGroup = serializers.PrimaryKeyRelatedField(many=True, queryset=models.RequestConfig.objects.all())

    class Meta:
        model = RequestGroup
        fields = ('id', 'name', 'RequestGroup')


class RequestGroupRetrieveSerializer(serializers.ModelSerializer):
    relationRequests = serializers.SerializerMethodField()
    RequestGroup = serializers.ReadOnlyField(source='id')

    def get_relationRequests(self, obj):
        RR = [RequestRelationSerializer(p).data for p in models.RequestRelation.objects.filter(request_group=obj.id)]
        RD = []
        for i in range(len(RR)):
            requestId = RR[i]['request_id']
            requestData = models.RequestConfig.objects.get(id=requestId)
            RC = RequestConfigSerializer(requestData).data
            RD.append(RC)
        return RD

    class Meta:
        model = RequestGroup
        fields = ('name', 'RequestGroup', 'relationRequests')


class RequestGroupCreateSerializer(serializers.ModelSerializer):
    relationRequests = RequestRelationSerializer(many=True, required=False)
    RequestGroup = serializers.ReadOnlyField(source='id')

    def create(self, validated_data):
        request_ids = validated_data.pop('relationRequests')
        request_group = models.RequestGroup.objects.create(**validated_data)
        for request_id in request_ids:
            d = dict(request_id)
            models.RequestRelation.objects.create(request_group=request_group, request_id=d['request_id'])
        return request_group

    class Meta:
        model = RequestGroup
        fields = ('name', 'RequestGroup', 'relationRequests')


class RequestGroupUpdateSerializer(serializers.ModelSerializer):
    relationRequests = RequestRelationSerializer(many=True, required=False)
    RequestGroup = serializers.ReadOnlyField(source='id')

    def update(self, instance, validated_data):
        request_ids = validated_data.pop('relationRequests')
        if request_ids:
            #     instance.RequestGroup.clear()
            #     for i in request_ids:
            #         RequestRelation.objects.create(request_id=i['request_id'], request_group=instance.id, name=i['name'],
            #                                        description=i['description'])
            # return super().update(instance, validated_data)

            for item in validated_data:
                if RequestGroup._meta.get_field(item):
                    setattr(instance, item, validated_data[item])
            RequestRelation.objects.filter(request_group=instance.id).delete()
            for request_id in request_ids:
                d = dict(request_id)
                models.RequestRelation.objects.create(request_group=instance.id, request_id=d['request_id'])
            instance.save()
        return instance

    class Meta:
        model = RequestGroup
        fields = ('name', 'RequestGroup', 'relationRequests')


class AutomationTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationTestResult
        fields = ('name', 'automationCaseApi', 'request_method', 'request_url', 'request_header', 'path_param_template',
                  'query_param_template', 'form_param_template', 'body_param_template',
                  'file_param_template', 'statusCode', 'result', 'responseData')


class ResultRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultRelation
        fields = ('name', 'request_id')


class ResultGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultGroup
        fields = ('id', 'name')


class ResultGroupRetrieveSerializer(serializers.ModelSerializer):
    relationRequests = serializers.SerializerMethodField()
    ResultGroup = serializers.ReadOnlyField(source='id')

    def get_relationRequests(self, obj):
        RR = [ResultRelationSerializer(p).data for p in models.ResultRelation.objects.filter(result_group=obj.id)]
        RD = []
        for i in range(len(RR)):
            requestId = RR[i]['request_id']
            resultData = models.AutomationTestResult.objects.get(automationCaseApi=requestId)
            RC = AutomationTestResultSerializer(resultData).data
            RD.append(RC)
        return RD

    class Meta:
        model = ResultGroup
        fields = ('name', 'ResultGroup', 'relationRequests')


class ResultGroupCreateSerializer(serializers.ModelSerializer):
    relationRequests = ResultRelationSerializer(many=True, required=False)
    ResultGroup = serializers.ReadOnlyField(source='id')

    def create(self, validated_data):
        request_ids = validated_data.pop('relationRequests')
        result_group = models.ResultGroup.objects.create(**validated_data)
        for request_id in request_ids:
            d = dict(request_id)
            models.ResultRelation.objects.create(result_group=result_group, request_id=d['request_id'])
        return result_group

    class Meta:
        model = ResultGroup
        fields = ('name', 'ResultGroup', 'relationRequests')


class ResultGroupUpdateSerializer(serializers.ModelSerializer):
    relationRequests = ResultRelationSerializer(many=True, required=False)
    ResultGroup = serializers.ReadOnlyField(source='id')

    def update(self, instance, validated_data):
        request_ids = validated_data.pop('relationRequests')
        if request_ids:
            #     instance.RequestGroup.clear()
            #     for i in request_ids:
            #         RequestRelation.objects.create(request_id=i['request_id'], request_group=instance.id, name=i['name'],
            #                                        description=i['description'])
            # return super().update(instance, validated_data)

            for item in validated_data:
                if ResultGroup._meta.get_field(item):
                    setattr(instance, item, validated_data[item])
            RequestRelation.objects.filter(request_group=instance.id).delete()
            for result in request_ids:
                d = dict(result)
                models.ResultGroup.objects.create(result_group=instance.id, request_id=d['request_id'])
            instance.save()
        return instance

    class Meta:
        model = ResultGroup
        fields = ('name', 'ResultGroup', 'relationRequests')


class StartAutoApiSerializer(serializers.ModelSerializer):
    request_group = serializers.ReadOnlyField(source='id')
    # market_channel_code = serializers.CharField()
    result_group = serializers.IntegerField()
    default_params_id=serializers.IntegerField

    class Meta:
        model = RequestGroup
        fields = ('request_group', 'result_group','default_params_id')


class AutomationReportSendConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationReportSendConfig
        fields = ("id", "projectResultGroup", 'reportFrom', 'mailUser', 'mailPass', 'mailSmtp')
