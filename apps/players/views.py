from rest_framework import generics
from rest_framework.serializers import ValidationError

from server.apps.rooms.models import RoomTime
from server.apps.rooms.serializers import RoomTimeSerializer
from server.core.abstract import StatsView

from .models import Player
from . import serializers


class PlayerListCreateView(StatsView, generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class PlayerRetrieveUpdateView(StatsView, generics.RetrieveUpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    lookup_field = 'username'

    def patch(self, request, username):
        if not request.user.is_active:
            raise ValidationError('You need to log in first.')

        if request.user.username != username:
            raise ValidationError('You are not the owner of this resource.')

        return super().patch(request, username)

    def puts(self, request, username):
        raise ValidationError('Use PATCH instead')


class RoomTimeListCreateView(StatsView, generics.ListCreateAPIView):
    queryset = RoomTime.objects.select_related('player', 'room', 'room__segment')
    serializer_class = RoomTimeSerializer

    def get_queryset(self):
        return self.queryset.filter(player__username=self.kwargs['username'])


class RoomTimeRetrieveUpdateDestroyView(StatsView, generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomTime.objects.select_related('player', 'room', 'room__segment')
    serializer_class = RoomTimeSerializer

    def get_queryset(self):
        return self.queryset.filter(player__username=self.kwargs['username'])

    def patch(self, request, username, pk):
        if not request.user.is_active:
            raise ValidationError('You need to log in first.')

        if request.user.username != username:
            raise ValidationError('You are not the owner of this resource.')

        return super().patch(request, username)

    def puts(self, request, *args, **kwargs):
        raise ValidationError('Use PATCH instead')
