# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-24 08:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meas', '0004_condition_serial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condition',
            name='lane',
        ),
        migrations.AddField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='lane',
            field=models.IntegerField(blank=True, default=999),
        ),
    ]
