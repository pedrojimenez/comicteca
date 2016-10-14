# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0032_comic_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comic',
            old_name='image',
            new_name='cover',
        ),
        migrations.AddField(
            model_name='comic',
            name='comments',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='comic',
            name='extrainfo',
            field=models.URLField(null=True, blank=True),
        ),
    ]
