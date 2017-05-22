# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 20:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0002_reportable_is_cluster_indicator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicatordataspecification',
            name='indicator',
        ),
        migrations.RemoveField(
            model_name='indicatordisaggregation',
            name='indicator',
        ),
        migrations.RemoveField(
            model_name='indicatorblueprint',
            name='cluster_activity',
        ),
        migrations.RemoveField(
            model_name='reportable',
            name='objective',
        ),
        migrations.RemoveField(
            model_name='reportable',
            name='project',
        ),
        migrations.DeleteModel(
            name='IndicatorDataSpecification',
        ),
        migrations.DeleteModel(
            name='IndicatorDisaggregation',
        ),
    ]
