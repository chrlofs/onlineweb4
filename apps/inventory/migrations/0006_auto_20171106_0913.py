# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-06 08:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_item_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemcategory',
            options={'permissions': (('view_itemcategory', 'View Item Category'),), 'verbose_name': 'Kategori', 'verbose_name_plural': 'Kategorier'},
        ),
    ]