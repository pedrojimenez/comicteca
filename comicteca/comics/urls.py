"""Urls for Comics app."""

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from comics import views
from comics.views import ArtistCreate, ArtistUpdate, ArtistDelete
from comics.views import ArtistListView
from comics.views import ColectionCreate, ColectionUpdate, ColectionDelete
from comics.views import ColectionListView
from comics.views import PublisherCreate, PublisherUpdate, PublisherDelete
from comics.views import PublisherListView
from comics.views import ComicListView
from comics.views import ComicCreate, ComicUpdate, ComicDelete

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    # ---------- #
    # artists
    # ---------- #
    url(r'^artists/(?P<artist_name_slug>[\w\-]+)/$', views.artist,
        name='artist_detail'),

    url(r'artists/add/$',
        login_required(ArtistCreate.as_view()),
        name='artist_add'),

    url(r'^artists/(?P<slug>[\w\-]+)/edit/$',
        login_required(ArtistUpdate.as_view()),
        name='artist_update'),

    url(r'^artists/(?P<slug>[\w\-]+)/delete/$',
        login_required(ArtistDelete.as_view()),
        name='artist_delete'),

    url(r'artists/$',
        login_required(ArtistListView.as_view()),
        name='artist_list'),

    # Deprecated:
    # url(r'^add_artist/$', views.add_artist, name='add_artist'),

    # ---------- #
    # colections
    # ---------- #
    url(r'colections/add/$',
        login_required(ColectionCreate.as_view()),
        name='colection_add'),

    url(r'^colections/(?P<colection_name_slug>[\w\-]+)/$',
        views.colection,
        name='colection_detail'),

    url(r'^colections/(?P<slug>[\w\-]+)/edit/$',
        login_required(ColectionUpdate.as_view()),
        name='colection_update'),

    url(r'^colections/(?P<slug>[\w\-]+)/add-comic/$',
        login_required(ComicCreate.as_view()),
        name='colection_comic_add'),

    url(r'^colections/(?P<slug>[\w\-]+)/delete/$',
        login_required(ColectionDelete.as_view()),
        name='colection_delete'),

    url(r'^add_colection/$',
        views.add_colection,
        name='add_colection'),

    url(r'colections/$',
        login_required(ColectionListView.as_view()),
        name='colection_list'),

    # ---------- #
    # publishers
    # ---------- #
    url(r'publishers/add/$',
        login_required(PublisherCreate.as_view()),
        name='publisher_add'),

    url(r'^publishers/(?P<publisher_name_slug>[\w\-]+)/$',
        views.publisher,
        name='publisher_detail'),

    url(r'^add_publisher/$',
        views.add_publisher,
        name='add_publisher'),

    url(r'^publishers/(?P<slug>[\w\-]+)/edit/$',
        login_required(PublisherUpdate.as_view()),
        name='publisher_update'),

    url(r'^publishers/(?P<slug>[\w\-]+)/delete/$',
        login_required(PublisherDelete.as_view()),
        name='publisher_delete'),

    url(r'publishers/$',
        login_required(PublisherListView.as_view()),
        name='publisher_list'),

    # ---------- #
    # comics
    # ---------- #
    url(r'comics/$',
        login_required(ComicListView.as_view()),
        name='comic_list'),

    url(r'comics/add/$',
        login_required(ComicCreate.as_view()),
        name='comic_add'),

    url(r'^comics/(?P<comic_name_slug>[\w\-]+)/$',
        views.comic,
        name='comic_detail'),

    url(r'^comics/(?P<slug>[\w\-]+)/edit/$',
        login_required(ComicUpdate.as_view()),
        name='comic_update'),

    url(r'^comics/(?P<slug>[\w\-]+)/delete/$',
        login_required(ComicDelete.as_view()),
        name='comic_delete'),

    # ---------- #
    # utils
    # ---------- #
    url(r'^about/$', views.about, name='about'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        name='login'),

    url(r'^logout_simple/$',
        'django.contrib.auth.views.logout',
        name='logout_simple'),

    url(r'^logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'),
)
