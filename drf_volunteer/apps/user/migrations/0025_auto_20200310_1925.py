# Generated by Django 2.2 on 2020-03-10 19:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_auto_20200219_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='logintime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 10, 19, 25, 10, 960287), help_text='注册时间', verbose_name='注册时间'),
        ),
    ]