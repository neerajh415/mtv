# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motor', '0006_auto_20160303_0724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='reporter',
        ),
    ]