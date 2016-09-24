# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import comics.storage


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0026_auto_20160917_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='colection',
            name='image',
            field=models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), upload_to=b'images/artists/'),
        ),
    ]
