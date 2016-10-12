# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutinator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'En gang'), (2, b'Gjentagende')]),
        ),
    ]
