# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 07:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_social_app', '0021_auto_20151229_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintain_history',
            name='maintain_time',
        ),
        migrations.AddField(
            model_name='maintain_history',
            name='maintain_approve_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 7, 9, 6, 49471, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='maintain_history',
            name='maintain_raise_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 7, 9, 6, 64580, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_schedule',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 7, 9, 6, 65153, tzinfo=utc)),
        ),
    ]
