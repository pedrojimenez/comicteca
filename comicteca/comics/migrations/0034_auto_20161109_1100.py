# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0033_auto_20161015_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='purchase_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='comic',
            name='purchase_unit',
            field=models.CharField(default=b'euros', max_length=15, verbose_name=b'Type', choices=[(b'euros', b'euros'), (b'pesetas', b'pesetas'), (b'dollars', b'dollars'), (b'pounds', b'pounds')]),
        ),
        migrations.AddField(
            model_name='comic',
            name='retail_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='comic',
            name='retail_unit',
            field=models.CharField(default=b'euros', max_length=15, verbose_name=b'Type', choices=[(b'euros', b'euros'), (b'pesetas', b'pesetas'), (b'dollars', b'dollars'), (b'pounds', b'pounds')]),
        ),
    ]
