import smtplib
from email.mime.text import MIMEText
from email.header import Header
from createData.models import AutomationReportSendConfig, ResultGroup
import django
import sys
import os


def sendEmail(result_group_id, data):
    """
    发送邮件
    :param project_id: 项目ID
    :param data: 发送内容
    :return:
    """
    # 第三方 SMTP 服务
    email_config = AutomationReportSendConfig.objects.filter(projectResultGroup=result_group_id)
    if email_config:
        mail_host = email_config[0].mailSmtp  # 设置服务器
        mail_user = email_config[0].mailUser  # 用户名
        mail_pass = email_config[0].mailPass  # 口令

        sender = email_config[0].reportFrom
        receivers = ['1534795944@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        message = MIMEText(data, 'plain', 'utf-8')
        message['From'] = email_config[0].reportFrom
        message['To'] = receivers[0]

        subject = ResultGroup.objects.filter(id=result_group_id)[0].name
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            return True
        except smtplib.SMTPException:
            return False
