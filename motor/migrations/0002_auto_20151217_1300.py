# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 13:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('motor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='email',
            field=models.EmailField(default='username@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mymodel',
            name='first_name',
            field=models.CharField(default='neeraj', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mymodel',
            name='last_name',
            field=models.CharField(default='default', max_length=30),
            preserve_default=False,
        ),
    ]
