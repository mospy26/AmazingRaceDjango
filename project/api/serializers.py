from django.contrib.auth.models import User
from rest_framework import serializers

from AmazingRaceApp.models import Game, Location, GamePlayer, GameCreator


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = (
            'title',
            'archived',
            'code',
            'live',
            'start_time',
            'end_time',
            'players'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class GamesPlayedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GamePlayer
        fields = (
            'rank',
            'game',
            'player'
        )


class GamesCreatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameCreator
        fields = '__all__'
