# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-30 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={'verbose_name': '权限表', 'verbose_name_plural': '权限表'},
        ),
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='图标'),
        ),
        migrations.AddField(
            model_name='permission',
            name='is_menu',
            field=models.BooleanField(default=False, verbose_name='是否是菜单'),
        ),
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='角色所拥有的权限'),
        ),
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='用户所拥有的角色'),
        ),
    ]
