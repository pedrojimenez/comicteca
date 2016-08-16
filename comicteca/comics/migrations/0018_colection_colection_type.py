# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0017_auto_20160813_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='colection',
            name='colection_type',
            field=models.CharField(default=b'Regular', max_length=15, verbose_name=b'Type', choices=[(b'Regular', b'Regular'), (b'Limited', b'Limited'), (b'Special', b'Special')]),
        ),
    ]
