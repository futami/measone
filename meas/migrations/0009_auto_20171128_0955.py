# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 00:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meas', '0008_auto_20171128_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='value',
            field=models.FloatField(blank=True),
        ),
    ]
