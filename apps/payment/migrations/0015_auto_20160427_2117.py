# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0014_auto_20160309_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='stripe_key',
            field=models.CharField(choices=[('prokom', 'prokom'), ('trikom', 'trikom'), ('arrkom', 'arrkom')], default='arrkom', max_length=10, verbose_name='stripe key'),
        ),
    ]