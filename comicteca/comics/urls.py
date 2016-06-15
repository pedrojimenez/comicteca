"""Urls for Comics app."""

from django.conf.urls import patterns, url
# from django.conf.urls import include

from comics import views
from comics.views import ArtistCreate, ArtistUpdate  # , ArtistDelete
from comics.views import ColectionCreate

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    # artists
    url(r'artists/add/$', ArtistCreate.as_view(), name='artist_add'),
    url(r'^artists/(?P<artist_name_slug>[\w\-]+)/$', views.artist,
        name='artist_detail'),
    url(r'^artists/(?P<slug>[\w\-]+)/edit/$',
        ArtistUpdate.as_view(), name='artist_update'),
    url(r'^add_artist/$', views.add_artist, name='add_artist'),

    # colections
    url(r'colections/add/$', ColectionCreate.as_view(), name='colection_add'),
    url(r'^colections/(?P<colection_name_slug>[\w\-]+)/$', views.colection,
        name='colection_detail'),
    url(r'^add_colection/$', views.add_colection, name='add_colection'),

    # publishers
    url(r'^publishers/(?P<publisher_name_slug>[\w\-]+)/$', views.publisher,
        name='publisher_detail'),
    url(r'^add_publisher/$', views.add_publisher, name='add_publisher'),

    # utils
    url(r'^about/$', views.about, name='about'),
)
