# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-25 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conversions', '0010_delete_conversions'),
    ]

    operations = [
        migrations.CreateModel(
            name='conversions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reverse_complement', models.BooleanField()),
            ],
        ),
    ]