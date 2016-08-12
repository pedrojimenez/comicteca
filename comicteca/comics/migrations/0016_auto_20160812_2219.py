# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0015_auto_20160812_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='colection',
            name='inserted',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='colection',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
