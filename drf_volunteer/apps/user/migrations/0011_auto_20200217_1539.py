# Generated by Django 2.2 on 2020-02-17 15:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20200216_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 17, 15, 39, 30, 306624), help_text='注册时间', verbose_name='注册时间'),
        ),
    ]
