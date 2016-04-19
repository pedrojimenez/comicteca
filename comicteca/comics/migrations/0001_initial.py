# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('deathdate', models.DateField(null=True, blank=True)),
                ('biography', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'artists',
                'verbose_name_plural': 'artists',
            },
        ),
    ]
