# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0041_auto_20161217_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='saga',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
    ]
