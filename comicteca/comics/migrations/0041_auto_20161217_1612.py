# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0040_auto_20161217_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComicsInSaga',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_in_saga', models.IntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='comic',
            name='sagas',
            field=models.ManyToManyField(related_name='Saga', through='comics.ComicsInSaga', to='comics.Saga'),
        ),
        migrations.AddField(
            model_name='comicsinsaga',
            name='comic',
            field=models.ForeignKey(to='comics.Comic'),
        ),
        migrations.AddField(
            model_name='comicsinsaga',
            name='saga',
            field=models.ForeignKey(to='comics.Saga'),
        ),
    ]
