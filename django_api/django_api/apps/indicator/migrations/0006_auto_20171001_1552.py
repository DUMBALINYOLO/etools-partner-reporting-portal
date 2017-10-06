# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 15:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0005_auto_20170929_1850'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicatorreport',
            options={'ordering': ['-due_date', '-id']},
        ),
        migrations.AlterField(
            model_name='indicatorreport',
            name='progress_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='indicator_reports', to='unicef.ProgressReport'),
        ),
    ]