# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-24 18:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversions', '0004_conversions_pattern_input'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversions',
            name='pattern_input',
        ),
    ]