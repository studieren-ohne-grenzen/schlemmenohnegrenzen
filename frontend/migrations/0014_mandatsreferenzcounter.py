# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0013_household_gpsstreet'),
    ]

    operations = [
        migrations.CreateModel(
            name='MandatsreferenzCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnt', models.IntegerField(default=0)),
            ],
        ),
    ]
