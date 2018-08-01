# coding: utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.RoomListView.as_view(),
        name='room_list'),
    url(r'^(?P<slug>.+)/$', views.RoomRetrieveView.as_view(),
        name='room_retrieve'),
]
