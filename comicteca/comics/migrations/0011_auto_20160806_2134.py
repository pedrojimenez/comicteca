# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0010_comic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='number',
            field=models.IntegerField(default=1, unique=True),
        ),
    ]
