# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-06 00:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unicef', '0009_auto_20190305_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progressreport',
            name='attachment',
        ),
    ]
