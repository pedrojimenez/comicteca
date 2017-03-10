# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0044_auto_20161221_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownership',
            name='purchase_unit',
            field=models.CharField(default=b'euros', max_length=15, verbose_name=b'Unit', choices=[(b'euros', b'euros'), (b'pesetas', b'pesetas'), (b'dollars', b'dollars'), (b'pounds', b'pounds')]),
        ),
    ]
