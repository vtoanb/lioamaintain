# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 02:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_social_app', '0019_auto_20151226_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintain_schedule',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 26, 2, 18, 3, 916759, tzinfo=utc)),
        ),
    ]
