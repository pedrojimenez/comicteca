# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0024_auto_20160917_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='nationality',
            field=django_countries.fields.CountryField(default=b'ES', max_length=2),
        ),
        migrations.AlterField(
            model_name='artist',
            name='nationality',
            field=django_countries.fields.CountryField(default=b'ES', max_length=2),
        ),
    ]
