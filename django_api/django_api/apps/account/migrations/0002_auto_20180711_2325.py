# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-11 23:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('partner', '0001_initial'),
        ('account', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='partner.Partner'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='workspaces',
            field=models.ManyToManyField(blank=True, help_text='These are workspaces that the user will be able to access.', related_name='users', to='core.Workspace'),
        ),
    ]
