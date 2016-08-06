"""Urls for Comics app."""

from django.conf.urls import patterns, url
# from django.conf.urls import include

from comics import views
from comics.views import ArtistCreate, ArtistUpdate, ArtistDelete
from comics.views import ArtistListView
from comics.views import ColectionCreate, ColectionUpdate, ColectionDelete
from comics.views import ColectionListView
from comics.views import PublisherCreate, PublisherUpdate, PublisherDelete
from comics.views import PublisherListView

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    # ---------- #
    # artists
    # ---------- #
    url(r'artists/add/$', ArtistCreate.as_view(), name='artist_add'),
    url(r'^artists/(?P<artist_name_slug>[\w\-]+)/$', views.artist,
        name='artist_detail'),

    url(r'^artists/(?P<slug>[\w\-]+)/edit/$',
        ArtistUpdate.as_view(), name='artist_update'),

    url(r'^artists/(?P<slug>[\w\-]+)/delete/$',
        ArtistDelete.as_view(), name='artist_delete'),

    url(r'^add_artist/$', views.add_artist, name='add_artist'),
    url(r'artists/$', ArtistListView.as_view(), name='artist_list'),

    # ---------- #
    # colections
    # ---------- #
    url(r'colections/add/$', ColectionCreate.as_view(), name='colection_add'),
    url(r'^colections/(?P<colection_name_slug>[\w\-]+)/$', views.colection,
        name='colection_detail'),

    url(r'^colections/(?P<slug>[\w\-]+)/edit/$',
        ColectionUpdate.as_view(), name='colection_update'),

    url(r'^colections/(?P<slug>[\w\-]+)/delete/$',
        ColectionDelete.as_view(), name='colection_delete'),

    url(r'^add_colection/$', views.add_colection, name='add_colection'),
    url(r'colections/$', ColectionListView.as_view(), name='colection_list'),

    # ---------- #
    # publishers
    # ---------- #
    url(r'publishers/add/$', PublisherCreate.as_view(), name='publisher_add'),

    url(r'^publishers/(?P<publisher_name_slug>[\w\-]+)/$', views.publisher,
        name='publisher_detail'),

    url(r'^add_publisher/$', views.add_publisher, name='add_publisher'),

    url(r'^publishers/(?P<slug>[\w\-]+)/edit/$',
        PublisherUpdate.as_view(), name='publisher_update'),

    url(r'^publishers/(?P<slug>[\w\-]+)/delete/$',
        PublisherDelete.as_view(), name='publisher_delete'),

    url(r'publishers/$', PublisherListView.as_view(), name='publisher_list'),

    # ---------- #
    # utils
    # ---------- #
    url(r'^about/$', views.about, name='about'),
)
