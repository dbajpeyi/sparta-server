# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 16:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Sport'),
        ),
    ]