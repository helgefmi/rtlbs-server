# coding: utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.StatsView.as_view(), name='stats_main'),
    url(r'^categories/$', views.CategoryListView.as_view(), name='stats_category_list'),
    url(r'^players/$', views.PlayerListView.as_view(), name='stats_player_list'),
    url(r'^runs/$', views.RunListView.as_view(), name='stats_run_list'),
]
