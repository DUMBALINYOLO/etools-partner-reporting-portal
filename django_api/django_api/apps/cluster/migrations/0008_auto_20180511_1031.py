# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-11 10:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0007_merge_20180405_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clusteractivity',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='clusterobjective',
            name='created_by',
        ),
    ]
