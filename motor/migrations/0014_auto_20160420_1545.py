# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-20 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motor', '0013_get_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cities', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='countries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='get_cities',
        ),
        migrations.AddField(
            model_name='cities',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motor.countries'),
        ),
    ]
