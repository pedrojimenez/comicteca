# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comics', '0043_auto_20161218_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchase_price', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='comic',
            name='users',
        ),
        migrations.AddField(
            model_name='ownership',
            name='comic',
            field=models.ForeignKey(to='comics.Comic'),
        ),
        migrations.AddField(
            model_name='ownership',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comic',
            name='my_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='comics.Ownership'),
        ),
        migrations.AlterUniqueTogether(
            name='ownership',
            unique_together=set([('comic', 'user')]),
        ),
    ]
