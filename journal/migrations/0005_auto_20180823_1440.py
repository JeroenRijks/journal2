# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-23 14:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_auto_20180823_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resource',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_tips', to=settings.AUTH_USER_MODEL),
        ),
    ]
