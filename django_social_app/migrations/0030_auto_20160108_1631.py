# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 09:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_social_app', '0029_auto_20160107_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='time_variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update_maintain', models.DateTimeField(default=datetime.datetime(2016, 1, 8, 9, 31, 14, 65601, tzinfo=utc))),
            ],
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_approve_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 8, 9, 31, 14, 79225, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_raise_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 8, 9, 31, 14, 79290, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_history',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 8, 9, 31, 14, 79353, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maintain_schedule',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 8, 9, 31, 14, 79918, tzinfo=utc)),
        ),
    ]
