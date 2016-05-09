# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0002_artist_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('subname', models.CharField(max_length=50, blank=True)),
                ('volume', models.IntegerField(default=1)),
                ('max_numbers', models.IntegerField(default=0)),
                ('numbers', models.IntegerField(default=0)),
                ('pub_date', models.DateField(null=True, blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'db_table': 'colections',
                'verbose_name_plural': 'colections',
            },
        ),
    ]
