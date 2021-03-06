import dateutil.parser

from django.http import JsonResponse

from rest_framework import generics
from rest_framework.views import APIView

from . import serializers
from .models import Category, Player, Run
from .utils import get_stats, get_leaderboards


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PlayerListView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class RunListView(generics.ListAPIView):
    queryset = Run.objects.all().select_related('player', 'moderator', 'category')
    serializer_class = serializers.RunSerializer


class StatsView(APIView):
    def dispatch(self, request):
        category = request.GET.get('category', 'all')
        stats = get_stats(category)
        return JsonResponse(stats)


class LeaderboardsView(APIView):
    def dispatch(self, request):
        category = request.GET['category']
        lbs_date = dateutil.parser.parse(request.GET['date']).date()

        lbs = get_leaderboards(category, lbs_date)
        return JsonResponse({
            'lbs': lbs,
        })
