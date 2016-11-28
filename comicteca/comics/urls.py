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
        login_required(ArtistCreate.as_view(
            template_name="comics/add_artist.html")),
        name='artist_add'),

    url(r'^artists/(?P<slug>[\w\-]+)/edit/$',
        login_required(ArtistUpdate.as_view(
            template_name="comics/update_artist_form.html")),
        name='artist_update'),

    url(r'^artists/(?P<slug>[\w\-]+)/delete/$',
        login_required(ArtistDelete.as_view(
            template_name="comics/delete_artist_confirm.html")),
        name='artist_delete'),

    url(r'artists/$',
        login_required(ArtistListView.as_view(
            template_name="comics/artist_list.html")),
        name='artist_list'),

    # Deprecated:
    # url(r'^add_artist/$', views.add_artist, name='add_artist'),

    # ---------- #
    # colections
    # ---------- #
    url(r'colections/add/$', ColectionCreate.as_view(), name='colection_add'),

    url(r'^colections/(?P<colection_name_slug>[\w\-]+)/$', views.colection,
        name='colection_detail'),

    url(r'^colections/(?P<slug>[\w\-]+)/edit/$',
        ColectionUpdate.as_view(), name='colection_update'),

    url(r'^colections/(?P<slug>[\w\-]+)/add-comic/$',
        ComicCreate.as_view(), name='colection_comic_add'),

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
    # comics
    # ---------- #
    url(r'comics/$', ComicListView.as_view(), name='comic_list'),

    url(r'comics/add/$', ComicCreate.as_view(), name='comic_add'),

    url(r'^comics/(?P<comic_name_slug>[\w\-]+)/$', views.comic,
        name='comic_detail'),

    url(r'^comics/(?P<slug>[\w\-]+)/edit/$',
        ComicUpdate.as_view(), name='comic_update'),

    url(r'^comics/(?P<slug>[\w\-]+)/delete/$',
        ComicDelete.as_view(), name='comic_delete'),

    # ---------- #
    # utils
    # ---------- #
    url(r'^about/$', views.about, name='about'),

    # ---------- #
    # utils
    # ---------- #
    url(r'^about/$', views.about, name='about'),

    url(r'^iilogin/$', views.user_login, name='iilogin'),

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
