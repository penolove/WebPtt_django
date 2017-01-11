from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^if/(?P<id>[0-9]*)$', views.Gossip_index, name='indexIF'),
    url(r'^if/(?P<id>[0-9]*)/(?P<date>.*)$', views.index_if, name='indexIF_date'),

]
