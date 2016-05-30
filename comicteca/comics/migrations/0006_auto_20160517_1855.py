# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0005_publisher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extrainfo', models.CharField(max_length=128, null=True, blank=True)),
                ('principal', models.BooleanField(default=True, verbose_name=b'Principal')),
                ('colection', models.ForeignKey(default=4, to='comics.Colection')),
                ('editorial', models.ForeignKey(to='comics.Publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extrainfo', models.CharField(max_length=128, null=True, blank=True)),
                ('principal', models.BooleanField(default=True, verbose_name=b'Principal')),
                ('colection', models.ForeignKey(default=4, to='comics.Colection')),
                ('editorial', models.ForeignKey(to='comics.Publisher')),
            ],
        ),
        migrations.AddField(
            model_name='colection',
            name='distributors',
            field=models.ManyToManyField(related_name='Distributors', through='comics.Distributor', to='comics.Publisher'),
        ),
        migrations.AddField(
            model_name='colection',
            name='editors',
            field=models.ManyToManyField(related_name='Publishers', through='comics.Editor', to='comics.Publisher'),
        ),
    ]
