# Generated by Django 2.2 on 2020-02-17 22:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20200217_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 17, 22, 1, 57, 605072), help_text='注册时间', verbose_name='注册时间'),
        ),
    ]
