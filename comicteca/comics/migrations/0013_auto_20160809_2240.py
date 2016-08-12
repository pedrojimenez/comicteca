# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0012_auto_20160808_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='comic',
            unique_together=set([('colection', 'number')]),
        ),
    ]
