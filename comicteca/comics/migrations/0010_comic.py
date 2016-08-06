# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0009_auto_20160806_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, null=True, blank=True)),
                ('number', models.IntegerField(default=1)),
                ('pages', models.IntegerField(default=24)),
                ('slug', models.SlugField()),
                ('extrainfo', models.CharField(max_length=128, null=True, blank=True)),
                ('colection', models.ForeignKey(to='comics.Colection')),
            ],
            options={
                'verbose_name_plural': 'comics',
            },
        ),
    ]
