# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-31 02:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_menu_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission'),
        ),
    ]
