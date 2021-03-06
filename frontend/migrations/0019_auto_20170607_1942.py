# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0018_auto_20170607_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='plz',
            field=models.IntegerField(choices=[(76131, '76131 (Innen- & Oststadt)'), (76133, '76133 (Innen-, Nord-, West-, Südweststadt)'), (76135, '76135 (West-, Südweststadt, Beiertheim-Bulach)'), (76137, '76137 (Südstadt, Südweststadt)'), (76139, '76139 (Hagsfeld, Waldstadt)'), (76149, '76149 (Nordstadt)'), (76185, '76185 (Mühlburg)'), (76187, '76187 (Nordweststadt)'), (76227, '76227 (Durlach)')], default=76133),
        ),
    ]
