# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import django.utils.timezone
from django.conf import settings
import comics.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('nationality', django_countries.fields.CountryField(default=b'ES', max_length=2)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('deathdate', models.DateField(null=True, blank=True)),
                ('biography', models.TextField(max_length=3000, null=True, blank=True)),
                ('inserted', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('extrainfo', models.URLField(null=True, blank=True)),
                ('image', models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), null=True, upload_to=b'images/artists/', blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ('-inserted',),
                'verbose_name_plural': 'artists',
            },
        ),
        migrations.CreateModel(
            name='Colaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extrainfo', models.CharField(max_length=128, null=True, blank=True)),
                ('role', models.CharField(default=b'Guion', max_length=15, choices=[(b'Guion', b'Guion'), (b'Dibujo', b'Dibujo'), (b'Tinta', b'Tinta'), (b'Color', b'Color'), (b'Color Ordenador', b'Color Ordenador'), (b'Dialogos', b'Dialogos'), (b'Portada', b'Portada'), (b'Argumento', b'Argumento'), (b'Adaptacion', b'Adaptacion')])),
                ('artist', models.ForeignKey(to='comics.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Colection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('subname', models.CharField(max_length=50, blank=True)),
                ('volume', models.IntegerField(default=1)),
                ('language', django_countries.fields.CountryField(default=b'ES', max_length=2)),
                ('max_numbers', models.IntegerField(default=0)),
                ('colection_type', models.CharField(default=b'Regular', max_length=15, verbose_name=b'Type', choices=[(b'Regular', b'Regular Serie'), (b'Limited', b'Limited Serie'), (b'Special', b'Special Number')])),
                ('colection_format', models.CharField(default=b'Grapa', max_length=15, verbose_name=b'Format', choices=[(b'Grapa', b'Grapa'), (b'Retapado', b'Retapado'), (b'Rustica', b'Rustica'), (b'Cartone', b'Cartone'), (b'Oversize', b'Oversize')])),
                ('numbers', models.IntegerField(default=0)),
                ('inserted', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), null=True, upload_to=b'images/colections/', blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'colections',
            },
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, null=True, blank=True)),
                ('number', models.IntegerField(default=1)),
                ('pages', models.IntegerField(default=24)),
                ('digital', models.BooleanField(default=False)),
                ('color', models.BooleanField(default=True)),
                ('slug', models.SlugField()),
                ('comments', models.TextField(default=b'', null=True, blank=True)),
                ('extrainfo', models.URLField(null=True, blank=True)),
                ('pub_date', models.DateField(null=True, blank=True)),
                ('inserted', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('purchase_price', models.FloatField(default=0)),
                ('purchase_unit', models.CharField(default=b'euros', max_length=15, verbose_name=b'Type', choices=[(b'euros', b'euros'), (b'pesetas', b'pesetas'), (b'dollars', b'dollars'), (b'pounds', b'pounds')])),
                ('retail_price', models.FloatField(default=0)),
                ('retail_unit', models.CharField(default=b'euros', max_length=15, verbose_name=b'Type', choices=[(b'euros', b'euros'), (b'pesetas', b'pesetas'), (b'dollars', b'dollars'), (b'pounds', b'pounds')])),
                ('cover', models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), null=True, upload_to=b'images/comics/', blank=True)),
                ('colaborators', models.ManyToManyField(to='comics.Artist', through='comics.Colaborator')),
                ('colection', models.ForeignKey(to='comics.Colection')),
            ],
            options={
                'verbose_name_plural': 'comics',
            },
        ),
        migrations.CreateModel(
            name='ComicsInSaga',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_in_saga', models.IntegerField(default=1)),
                ('comic', models.ForeignKey(to='comics.Comic')),
            ],
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchase_price', models.FloatField(default=0)),
                ('purchase_unit', models.CharField(default=b'euros', max_length=15, verbose_name=b'Unit', choices=[(b'euros', b'euros'), (b'pesetas', b'pesetas'), (b'dollars', b'dollars'), (b'pounds', b'pounds')])),
                ('comic', models.ForeignKey(to='comics.Comic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('photo', models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), null=True, upload_to=b'images/users/', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('nationality', django_countries.fields.CountryField(default=b'ES', max_length=2)),
                ('history', models.TextField(default=b'', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name=b'Comienzo de Editorial', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name=b'Fin de Publicaciones', blank=True)),
                ('inserted', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('extrainfo', models.URLField(null=True, blank=True)),
                ('image', models.ImageField(default=b'', storage=comics.storage.OverwriteStorage(), null=True, upload_to=b'images/publishers/', blank=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Saga',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('total_numbers', models.IntegerField(default=1)),
                ('argument', models.TextField(max_length=3000, null=True, blank=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='comicsinsaga',
            name='saga',
            field=models.ForeignKey(to='comics.Saga'),
        ),
        migrations.AddField(
            model_name='comic',
            name='my_sagas',
            field=models.ManyToManyField(to='comics.Saga', through='comics.ComicsInSaga'),
        ),
        migrations.AddField(
            model_name='comic',
            name='my_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='comics.Ownership'),
        ),
        migrations.AddField(
            model_name='colection',
            name='distributor',
            field=models.ForeignKey(default=1, to='comics.Publisher'),
        ),
        migrations.AddField(
            model_name='colection',
            name='editors',
            field=models.ManyToManyField(related_name='Publishers', to='comics.Publisher'),
        ),
        migrations.AddField(
            model_name='colaborator',
            name='comic',
            field=models.ForeignKey(to='comics.Comic'),
        ),
        migrations.AlterUniqueTogether(
            name='artist',
            unique_together=set([('name', 'nationality', 'birthdate')]),
        ),
        migrations.AlterUniqueTogether(
            name='ownership',
            unique_together=set([('comic', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='comicsinsaga',
            unique_together=set([('saga', 'number_in_saga')]),
        ),
        migrations.AlterUniqueTogether(
            name='comic',
            unique_together=set([('colection', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='colection',
            unique_together=set([('name', 'volume')]),
        ),
        migrations.AlterUniqueTogether(
            name='colaborator',
            unique_together=set([('comic', 'artist', 'role')]),
        ),
    ]
