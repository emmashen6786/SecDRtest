# Generated by Django 2.2.1 on 2019-06-20 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('createData', '0002_automationreportsendconfig'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='automationreportsendconfig',
            options={'ordering': ['id'], 'verbose_name': '邮件发送配置', 'verbose_name_plural': '邮件发送配置'},
        ),
        migrations.RemoveField(
            model_name='automationreportsendconfig',
            name='description',
        ),
        migrations.RemoveField(
            model_name='automationreportsendconfig',
            name='name',
        ),
        migrations.AlterModelTable(
            name='automationreportsendconfig',
            table='automation_report_send_config',
        ),
    ]
