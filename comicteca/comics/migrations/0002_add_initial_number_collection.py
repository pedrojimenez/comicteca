# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='colection',
            name='initial_number',
            field=models.IntegerField(default=1),
        ),
    ]
