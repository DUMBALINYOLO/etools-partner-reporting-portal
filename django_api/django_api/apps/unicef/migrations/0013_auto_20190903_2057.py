# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-03 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unicef', '0012_auto_20190507_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmedocument',
            name='funds_received_to_date_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True, verbose_name='Funds received %'),
        ),
        migrations.AlterField(
            model_name='programmedocument',
            name='funds_received_to_date',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True, verbose_name='Funds received'),
        ),
    ]
