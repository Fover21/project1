# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-31 02:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20181030_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='weight',
            field=models.IntegerField(default=1),
        ),
    ]
