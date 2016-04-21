# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-02 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motor', '0002_auto_20151217_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='year_in_school',
            field=models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')], default='FR', max_length=2),
        ),
    ]