# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-26 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20180305_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='DEFAULT_FIRST_NAME', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='DEFAULT_LAST_NAME', max_length=64),
            preserve_default=False,
        ),
    ]