# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-06 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0004_auto_20170530_0348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clusteractivity',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='clusterobjective',
            options={'ordering': ['id']},
        ),
    ]
