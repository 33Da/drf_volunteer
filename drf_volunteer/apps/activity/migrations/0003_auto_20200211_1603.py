# Generated by Django 2.2 on 2020-02-11 16:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20200210_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userandactivity',
            name='signtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 11, 16, 3, 33, 7347), help_text='报名时间', verbose_name='报名时间'),
        ),
    ]