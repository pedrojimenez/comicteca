# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0018_colection_colection_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extrainfo', models.CharField(max_length=128, null=True, blank=True)),
                ('role', models.CharField(default=b'Guion', max_length=15, choices=[(b'Guion', b'Guion'), (b'Dibujo', b'Dibujo'), (b'Tinta', b'Tinta'), (b'Color', b'Color'), (b'Color Ordenador', b'Color Ordenador'), (b'Dialogos', b'Dialogos'), (b'Portada', b'Portada'), (b'Argumento', b'Argumento'), (b'Adaptacion', b'Adaptacion')])),
                ('artist', models.ForeignKey(to='comics.Artist')),
                ('comic', models.ForeignKey(to='comics.Comic')),
            ],
        ),
        migrations.AlterField(
            model_name='colection',
            name='colection_type',
            field=models.CharField(default=b'Regular', max_length=15, verbose_name=b'Type', choices=[(b'Regular', b'Regular Serie'), (b'Limited', b'Limited Serie'), (b'Special', b'Special Number')]),
        ),
        migrations.AddField(
            model_name='comic',
            name='colaborators',
            field=models.ManyToManyField(to='comics.Artist', through='comics.Colaborator'),
        ),
        migrations.AlterUniqueTogether(
            name='colaborator',
            unique_together=set([('comic', 'artist', 'role')]),
        ),
    ]
