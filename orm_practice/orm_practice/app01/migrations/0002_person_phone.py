# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-11 01:34
from __future__ import unicode_literals

import app01.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone',
            field=app01.models.MyCharField(default=15522031773, max_length=11),
            preserve_default=False,
        ),
    ]