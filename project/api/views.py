from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from .serializers import GameSerializer, UserSerializer, LocationSerializer, GamesPlayedSerializer, \
    GamesCreatorSerializer
from AmazingRaceApp.models import Game, Location, GamePlayer, GameCreator


class GameView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = Game.objects.all().order_by('title')
    serializer_class = GameSerializer


class UserView(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LocationView(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class GamesPlayedView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = GamePlayer.objects.none()
    serializer_class = GamesPlayedSerializer

    def list(self, request, **kwargs):
        games_played = GamePlayer.objects.filter(player=request.user)
        serializer = GamesPlayedSerializer(games_played, many=True, context={'request': request})
        return Response(serializer.data)


class GamesCreatedView(viewsets.ModelViewSet):
    queryset = GameCreator.objects.none()
    serializer_class = GamesCreatorSerializer

    def list(self, request, **kwargs):
        games_played = GamePlayer.objects.filter(player=request.user)
        serializer = GamesPlayedSerializer(games_played, many=True, context={'request': request})
        return Response(serializer.data)