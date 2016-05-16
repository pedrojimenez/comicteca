# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0004_colection_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('name', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('history', models.TextField(default=b'', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name=b'Comienzo de Editorial', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name=b'Fin de Publicaciones', blank=True)),
                ('slug', models.SlugField()),
            ],
        ),
    ]
