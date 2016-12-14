# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0037_colection_colection_format'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colection',
            name='pub_date',
        ),
        migrations.AlterField(
            model_name='colection',
            name='colection_format',
            field=models.CharField(default=b'Grapa', max_length=15, verbose_name=b'Format', choices=[(b'Grapa', b'Grapa'), (b'Retapado', b'Retapado'), (b'Rustica', b'Rustica'), (b'Cartone', b'Cartone'), (b'Oversize', b'Oversize')]),
        ),
    ]
