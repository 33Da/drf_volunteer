# Generated by Django 2.2 on 2020-02-19 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20200218_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='activity_time',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 19, 12, 57, 8, 382375), help_text='注册时间', verbose_name='注册时间'),
        ),
    ]
