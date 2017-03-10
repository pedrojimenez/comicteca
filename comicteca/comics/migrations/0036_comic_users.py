# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comics', '0035_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='users',
            field=models.ManyToManyField(related_name='Users', to=settings.AUTH_USER_MODEL),
        ),
    ]
