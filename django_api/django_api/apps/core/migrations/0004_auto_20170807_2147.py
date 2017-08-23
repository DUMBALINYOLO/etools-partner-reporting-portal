# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_responseplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='reportable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='indicator.Reportable'),
        ),
    ]