# Generated by Django 2.2 on 2020-02-15 17:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200215_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 15, 17, 57, 21, 792680), help_text='注册时间', verbose_name='注册时间'),
        ),
    ]
