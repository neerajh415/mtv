# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-20 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motor', '0012_auto_20160417_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='get_cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200)),
                ('cities', models.CharField(max_length=200)),
            ],
        ),
    ]