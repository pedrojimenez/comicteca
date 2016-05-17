from django.conf.urls import patterns, url
from django.conf.urls import include

from comics import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^artists/(?P<artist_name_slug>[\w\-]+)/$', views.artist, name='artist'),
    url(r'^add_artist/$', views.add_artist, name='add_artist'),
    url(r'^colections/(?P<colection_name_slug>[\w\-]+)/$', views.colection, name='colection'),
    url(r'^add_colection/$', views.add_colection, name='add_colection'),
    url(r'^publishers/(?P<publisher_name_slug>[\w\-]+)/$', views.publisher, name='publisher'),
    url(r'^add_publisher/$', views.add_publisher, name='add_publisher'),
    url(r'^about/$', views.about, name='about'),
)
