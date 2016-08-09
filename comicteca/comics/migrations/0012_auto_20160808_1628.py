# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0011_auto_20160806_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colection',
            old_name='distributors',
            new_name='distributor',
        ),
    ]
