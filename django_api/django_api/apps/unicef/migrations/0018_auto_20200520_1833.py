# Generated by Django 2.2.12 on 2020-05-20 18:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unicef', '0017_auto_20191107_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmedocument',
            name='amendments',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
