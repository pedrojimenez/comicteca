# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0006_auto_20160531_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colection',
            name='distributors',
        ),
        migrations.AddField(
            model_name='colection',
            name='distributors',
            field=models.ForeignKey(default=b'Marvel', to='comics.Publisher'),
        ),
        migrations.AlterUniqueTogether(
            name='artist',
            unique_together=set([('name', 'nationality', 'birthdate')]),
        ),
    ]
