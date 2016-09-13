# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import comics.storage


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0021_auto_20160905_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), upload_to=b'images/artists/'),
        ),
    ]
