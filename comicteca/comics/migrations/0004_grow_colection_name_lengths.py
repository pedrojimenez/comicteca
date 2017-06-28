# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0003_Add_distributor_to_collection_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colection',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='colection',
            name='subname',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
