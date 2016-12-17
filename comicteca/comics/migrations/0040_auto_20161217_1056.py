# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0039_auto_20161216_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saga',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('total_numbers', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='comic',
            name='sagas',
            field=models.ManyToManyField(related_name='Saga', to='comics.Saga'),
        ),
    ]
