# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
