# Generated by Django 2.2 on 2020-02-18 20:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20200218_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 18, 20, 51, 57, 165260), help_text='注册时间', verbose_name='注册时间'),
        ),
    ]
