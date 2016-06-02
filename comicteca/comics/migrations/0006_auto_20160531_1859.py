# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0005_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='colection',
            name='distributors',
            field=models.ManyToManyField(related_name='Distributors', to='comics.Publisher'),
        ),
        migrations.AddField(
            model_name='colection',
            name='editors',
            field=models.ManyToManyField(related_name='Publishers', to='comics.Publisher'),
        ),
        migrations.AlterUniqueTogether(
            name='colection',
            unique_together=set([('name', 'volume')]),
        ),
    ]
