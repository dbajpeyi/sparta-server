# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20160130_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleaction',
            name='is_liked',
            field=models.BooleanField(db_index=True),
        ),
    ]
