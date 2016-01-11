# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 09:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_social_app', '0027_auto_20151229_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='last_name',
        ),
        migrations.AddField(
            model_name='staff',
            name='username',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_approve_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 9, 27, 2, 264388, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_raise_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 9, 27, 2, 279064, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 9, 27, 2, 279108, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_schedule',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 9, 27, 2, 279672, tzinfo=utc)),
        ),
    ]
