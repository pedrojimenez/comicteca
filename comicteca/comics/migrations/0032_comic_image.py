# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import comics.storage


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0031_auto_20161014_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='image',
            field=models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), null=True, upload_to=b'images/comics/', blank=True),
        ),
    ]
