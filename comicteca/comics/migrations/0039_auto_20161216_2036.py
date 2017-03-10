# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0038_auto_20161214_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='color',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comic',
            name='digital',
            field=models.BooleanField(default=False),
        ),
    ]
