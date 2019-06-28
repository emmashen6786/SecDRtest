from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'requestconfig', views.RequestViewSet)
router.register(r'responseconfig', views.ResponseViewSet)
router.register(r'publicParam', views.DefaultPublicParamViewSet)
router.register(r'request_group', views.RequestGroupViewSet)
router.register(r'request_relation', views.RequestRelationViewSet)
router.register(r'request_group_easy', views.RequestGroupEasyViewSet)
router.register(r'test_result', views.AutomationTestResultViewSet)
router.register(r'result_group', views.ResultGroupViewSet)
router.register(r'result_relation', views.ResultRelationViewSet)
router.register(r'automation_report_send_config', views.AutomationReportSendConfigViewSet)
