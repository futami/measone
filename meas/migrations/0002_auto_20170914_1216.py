# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'entries'},
        ),
        migrations.AlterField(
            model_name='entry',
            name='unit',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
