# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0019_auto_20160821_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='pub_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
