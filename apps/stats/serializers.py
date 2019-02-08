from rest_framework import serializers

from .models import Category, Player, Run


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'type',
        ]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'id',
            'link',
            'signed_up',
            'location',
            'twitch_url',
        ]


class RunSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    class Meta:
        model = Run
        fields = [
            'id',
            'link',
            'comment',
            'status',
            'date',
            'emulated',
        ]

    def get_category(self, obj):
        return CategorySerializer(obj).data

    def get_player(self, obj):
        return PlayerSerializer(obj).data

    def get_moderator(self, obj):
        return PlayerSerializer(obj).data
