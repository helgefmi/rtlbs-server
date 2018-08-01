# coding: utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    # Players
    url(r'^$', views.PlayerListCreateView.as_view(), name='player_list_create'),
    url(r'^(?P<username>\w+)/$', views.PlayerRetrieveUpdateView.as_view(), name='player_retrieve_update'),

    # Room times
    url(r'^(?P<username>\w+)/roomtimes/$', views.RoomTimeListCreateView.as_view(),
        name='player_list_roomtime_view'),
    url(r'^(?P<username>\w+)/roomtimes/(?P<pk>\d+)/$', views.RoomTimeRetrieveUpdateDestroyView.as_view(),
        name='player_list_roomtime_view'),
]
