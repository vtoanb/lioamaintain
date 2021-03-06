# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 08:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_social_app', '0011_auto_20151221_0836'),
    ]

    operations = [
        migrations.CreateModel(
            name='energy_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('energy', models.IntegerField()),
                ('save_time', models.DateTimeField(verbose_name='energy save time')),
            ],
        ),
        migrations.CreateModel(
            name='machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_name', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(verbose_name='created date')),
                ('energy_today', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='maintain_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintain_type', models.IntegerField()),
                ('maintain_time', models.DateTimeField(verbose_name='maintain save time')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_social_app.machine')),
            ],
        ),
        migrations.CreateModel(
            name='maintain_schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintain_time', models.DateTimeField(verbose_name='maintain time')),
                ('maintain_type', models.IntegerField(verbose_name='maintain type')),
                ('maintain_time_remain', models.IntegerField(default=1000)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_social_app.machine')),
            ],
        ),
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('manager', models.BooleanField()),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='maintain_history',
            name='maintainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_social_app.staff'),
        ),
        migrations.AddField(
            model_name='energy_history',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_social_app.machine'),
        ),
    ]
