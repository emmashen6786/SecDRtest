from django.db import models

REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)
HTTP_CODE_CHOICE = (
    ('200', '200'),
    ('404', '404'),
    ('400', '400'),
    ('502', '502'),
    ('500', '500'),
    ('302', '302'),
)
RESULT_CHOICE = (
    ('PASS', '成功'),
    ('FAIL', '失败'),
)


class BaseModel(models.Model):
    """
    基础模型
    """
    name = models.CharField(max_length=255, default='', verbose_name='名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class RequestConfig(BaseModel):
    """
    接口请求基本配置
    """
    id = models.AutoField(primary_key=True)
    request_method = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    request_url = models.TextField(blank=True, null=True, verbose_name='接口地址')
    request_header = models.TextField(blank=True, null=True, verbose_name='请求头文件')
    path_param_template = models.TextField(blank=True, null=True, verbose_name='url中的参数')
    query_param_template = models.TextField(blank=True, null=True, verbose_name='问号后的参数')
    form_param_template = models.TextField(blank=True, null=True, verbose_name='表单格式的参数')
    body_param_template = models.TextField(blank=True, null=True, verbose_name='raw格式的参数')
    file_param_template = models.TextField(blank=True, null=True, verbose_name='文件格式的参数')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'request_config'


class ResponseConfig(BaseModel):
    """
    接口请求期待结果配置
    """
    id = models.AutoField(primary_key=True)
    related_reqid = models.ForeignKey(RequestConfig, on_delete=models.CASCADE, verbose_name="期待返回值对应的请求id")
    dependent_param_list = models.TextField(blank=True, null=True, verbose_name='接口返回值里保存全局参数')
    expect_response = models.TextField(blank=True, null=True, verbose_name='期待结果')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'response_config'


class DefaultPublicParam(BaseModel):
    """
    默认全局公共参数
    """
    id = models.AutoField(primary_key=True)
    channel_id = models.IntegerField(null=True, verbose_name='channel_id')
    product_code = models.CharField(max_length=50, verbose_name='一级产品code')
    sub_product_code = models.CharField(max_length=50, verbose_name='二级产品code')
    market_channel_code = models.CharField(max_length=50, verbose_name='渠道code')
    publice_params = models.TextField(blank=True, null=True, verbose_name='公共参数')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'default_public_param'


class RequestGroup(BaseModel):
    """
    请求组
    """
    id = models.AutoField(primary_key=True)
    RequestGroup = models.ManyToManyField(RequestConfig, through='RequestRelation', verbose_name='请求id列表')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'request_group'


class RequestRelation(BaseModel):
    """
    请求与组的三方表
    """
    id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(RequestConfig, on_delete=models.CASCADE)
    request_group = models.ForeignKey(RequestGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.request_id.name + "" + self.request_group.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'request_relation'
        # auto_created = True


class AutomationTestResult(BaseModel):
    """
    每个接口的执行结果
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.OneToOneField(RequestConfig, on_delete=models.CASCADE, verbose_name='接口')
    request_method = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    request_url = models.TextField(blank=True, null=True, verbose_name='接口地址')
    request_header = models.TextField(blank=True, null=True, verbose_name='请求头文件')
    path_param_template = models.TextField(blank=True, null=True, verbose_name='url中的参数')
    query_param_template = models.TextField(blank=True, null=True, verbose_name='问号后的参数')
    form_param_template = models.TextField(blank=True, null=True, verbose_name='表单格式的参数')
    body_param_template = models.TextField(blank=True, null=True, verbose_name='raw格式的参数')
    file_param_template = models.TextField(blank=True, null=True, verbose_name='文件格式的参数')
    statusCode = models.CharField(blank=True, null=True, max_length=1024, verbose_name='期望HTTP状态',
                                  choices=HTTP_CODE_CHOICE)
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'automation_test_result'


class ResultGroup(BaseModel):
    """
    结果组
    """
    id = models.AutoField(primary_key=True)
    ResultGroup = models.ManyToManyField(RequestConfig, through='ResultRelation', verbose_name='每组api结果列表')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'result_group'


class ResultRelation(BaseModel):
    """
    api与结果组的三方表
    """
    id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(RequestConfig, on_delete=models.CASCADE)
    result_group = models.ForeignKey(ResultGroup, on_delete=models.CASCADE, verbose_name='组')

    def __str__(self):
        return self.request_id.name + "" + self.result_group.name

    class Meta:
        ordering = ['updated_time']
        db_table = 'result_relation'

class AutomationReportSendConfig(models.Model):
    """
    报告发送人配置
    """
    id = models.AutoField(primary_key=True)
    projectResultGroup = models.OneToOneField(ResultGroup, on_delete=models.CASCADE, verbose_name="项目")
    reportFrom = models.EmailField(max_length=1024, blank=True, null=True, verbose_name="发送人邮箱")
    mailUser = models.CharField(max_length=1024, blank=True, null=True, verbose_name="用户名")
    mailPass = models.CharField(max_length=1024, blank=True, null=True, verbose_name="口令")
    mailSmtp = models.CharField(max_length=1024, blank=True, null=True, verbose_name="邮箱服务器")
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.reportFrom

    class Meta:
        verbose_name = "邮件发送配置"
        verbose_name_plural = "邮件发送配置"
        ordering = ['id']
        db_table = 'automation_report_send_config'


