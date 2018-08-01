from rest_framework import generics

from server.core.abstract import StatsView

from . import serializers
from .models import Room, RoomTime


class RoomListView(StatsView, generics.ListAPIView):
    queryset = Room.objects.all().select_related('segment')
    serializer_class = serializers.RoomSummarySerializer


class RoomRetrieveView(StatsView, generics.RetrieveAPIView):
    queryset = Room.objects.all().select_related('segment')
    serializer_class = serializers.RoomDetailSerializer
    lookup_field = 'slug'


class LatestRoomtimeListView(StatsView, generics.ListAPIView):
    serializer_class = serializers.RoomTimeSerializer

    def get_queryset(self):
        qset = RoomTime.objects.select_related('player', 'room', 'room__segment')

        last_id = self.request.GET.get('lastId')
        if last_id:
            rt = RoomTime.objects.get(pk=int(last_id))
            qset = qset.filter(datetime_updated__lt=rt.datetime_updated)

        return qset.order_by('-datetime_updated')[:20]
