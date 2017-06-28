# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0002_add_initial_number_collection'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='colection',
            unique_together=set([('name', 'volume', 'distributor')]),
        ),
    ]
