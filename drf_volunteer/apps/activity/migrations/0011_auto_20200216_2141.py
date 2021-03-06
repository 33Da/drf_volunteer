# Generated by Django 2.2 on 2020-02-16 21:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_auto_20200216_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='ativity',
            name='no_check',
            field=models.CharField(blank=True, help_text='不通过意见', max_length=200, null=True, verbose_name='不通过意见'),
        ),
        migrations.AlterField(
            model_name='ativity',
            name='createtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 16, 21, 41, 21, 697554), help_text='创建时间', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='userandactivity',
            name='signtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 16, 21, 41, 21, 698553), help_text='报名时间', verbose_name='报名时间'),
        ),
    ]
