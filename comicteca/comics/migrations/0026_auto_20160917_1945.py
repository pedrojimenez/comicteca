# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import comics.storage


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0025_auto_20160917_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='image',
            field=models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), upload_to=b'images/publishers/'),
        ),
    ]
