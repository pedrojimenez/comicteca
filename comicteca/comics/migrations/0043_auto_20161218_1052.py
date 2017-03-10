# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0042_saga_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='saga',
            name='argument',
            field=models.TextField(max_length=3000, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='comicsinsaga',
            unique_together=set([('saga', 'number_in_saga')]),
        ),
    ]
