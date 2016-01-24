# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-24 20:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_profile_gravatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.AlterModelManagers(
            name='profile',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
