# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.FloatField()),
                ('temperature', models.FloatField()),
            ],
        ),
    ]
