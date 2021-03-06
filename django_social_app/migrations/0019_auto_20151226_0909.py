# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 02:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_social_app', '0018_auto_20151224_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='counter_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField()),
                ('energy', models.IntegerField()),
                ('save_time', models.DateTimeField(verbose_name='counter save time')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_social_app.machine')),
            ],
        ),
        migrations.AlterField(
            model_name='maintain_schedule',
            name='maintain_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 26, 2, 9, 14, 694146, tzinfo=utc)),
        ),
    ]
