# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import comics.storage


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0023_auto_20160913_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='extrainfo',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='publisher',
            name='image',
            field=models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), upload_to=b'images/artists/'),
        ),
    ]
