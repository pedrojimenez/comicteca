# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0003_colection'),
    ]

    operations = [
        migrations.AddField(
            model_name='colection',
            name='language',
            field=django_countries.fields.CountryField(default=b'ES', max_length=2),
        ),
    ]
