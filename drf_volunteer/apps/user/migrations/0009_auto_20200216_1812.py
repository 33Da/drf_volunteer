# Generated by Django 2.2 on 2020-02-16 18:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20200216_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 16, 18, 12, 46, 931566), help_text='注册时间', verbose_name='注册时间'),
        ),
    ]
