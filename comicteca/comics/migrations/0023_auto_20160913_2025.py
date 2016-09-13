# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0022_auto_20160913_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='biography',
            field=models.TextField(max_length=3000, null=True, blank=True),
        ),
    ]
