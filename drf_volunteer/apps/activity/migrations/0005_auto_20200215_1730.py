# Generated by Django 2.2 on 2020-02-15 17:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20200215_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativity',
            name='createtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 15, 17, 30, 14, 88105), help_text='创建时间', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='userandactivity',
            name='signtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 15, 17, 30, 14, 89101), help_text='报名时间', verbose_name='报名时间'),
        ),
    ]
