# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 09:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_social_app', '0025_auto_20151229_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_approve_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 9, 21, 1, 49263, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_raise_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 9, 21, 1, 62955, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 9, 21, 1, 63001, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_schedule',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 9, 21, 1, 63622, tzinfo=utc)),
        ),
    ]
