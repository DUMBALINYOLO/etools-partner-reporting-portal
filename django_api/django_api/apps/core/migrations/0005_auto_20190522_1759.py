# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-22 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20181024_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='external_source',
            field=models.TextField(blank=True, choices=[('HPC', 'HPC'), ('OPS', 'OPS'), ('UNICEF', 'UNICEF')], null=True),
        ),
        migrations.AlterField(
            model_name='prprole',
            name='external_source',
            field=models.TextField(blank=True, choices=[('HPC', 'HPC'), ('OPS', 'OPS'), ('UNICEF', 'UNICEF')], null=True),
        ),
        migrations.AlterField(
            model_name='responseplan',
            name='external_source',
            field=models.TextField(blank=True, choices=[('HPC', 'HPC'), ('OPS', 'OPS'), ('UNICEF', 'UNICEF')], null=True),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='external_source',
            field=models.TextField(blank=True, choices=[('HPC', 'HPC'), ('OPS', 'OPS'), ('UNICEF', 'UNICEF')], null=True),
        ),
    ]
