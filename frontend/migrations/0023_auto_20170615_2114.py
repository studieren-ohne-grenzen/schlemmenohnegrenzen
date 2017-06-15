# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0022_auto_20170612_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitinggroup',
            name='dinner',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='visitinggroup',
            name='gastgeber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.Household'),
        ),
    ]
