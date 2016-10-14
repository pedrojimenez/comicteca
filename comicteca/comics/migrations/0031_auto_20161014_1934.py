# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import comics.storage


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0030_auto_20161013_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colection',
            name='image',
            field=models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), null=True, upload_to=b'images/colections/', blank=True),
        ),
    ]
