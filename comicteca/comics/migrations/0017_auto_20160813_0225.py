# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0016_auto_20160812_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='inserted',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comic',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
