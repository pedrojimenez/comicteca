# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0013_auto_20160809_2240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ('-inserted',), 'verbose_name_plural': 'artists'},
        ),
        migrations.AddField(
            model_name='artist',
            name='inserted',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
