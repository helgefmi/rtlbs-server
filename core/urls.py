from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from server.apps.rooms.views import LatestRoomtimeListView

urlpatterns = [
    url(r'^jwt/obtain/', obtain_jwt_token),
    url(r'^jwt/refresh/', refresh_jwt_token),

    url(r'^players/', include('server.apps.players.urls')),
    url(r'^rooms/', include('server.apps.rooms.urls')),
    url(r'^stats/', include('server.apps.stats.urls')),

    url(r'^latest-roomtimes/$', LatestRoomtimeListView.as_view(),
        name='roomtime_latest_list'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
