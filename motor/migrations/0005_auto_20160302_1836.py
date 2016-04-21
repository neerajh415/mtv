# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 18:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('motor', '0004_auto_20160205_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelManagers(
            name='mymodel',
            managers=[
                ('people', django.db.models.manager.Manager()),
            ],
        ),
    ]
