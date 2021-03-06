# Generated by Django 2.2 on 2020-02-15 17:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20200215_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='ativity',
            name='registration_endtime',
            field=models.DateField(blank=True, help_text='报名结束时间', null=True, verbose_name='报名结束时间'),
        ),
        migrations.AlterField(
            model_name='ativity',
            name='createtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 15, 17, 57, 21, 801642), help_text='创建时间', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='userandactivity',
            name='signtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 15, 17, 57, 21, 802641), help_text='报名时间', verbose_name='报名时间'),
        ),
    ]
