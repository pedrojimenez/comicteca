# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0020_comic_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='extrainfo',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ImageField(default=b'', upload_to=b'images/artists/'),
        ),
    ]
