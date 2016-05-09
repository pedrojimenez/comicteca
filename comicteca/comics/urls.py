from django.conf.urls import patterns, url
from django.conf.urls import include

from comics import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^artist/(?P<artist_name_slug>[\w\-]+)/$', views.artist, name='artist'),
    url(r'^colection/(?P<colection_name_slug>[\w\-]+)/$', views.colection, name='colection'),
    #url(r'^about/$', views.about, name='about'),
)
