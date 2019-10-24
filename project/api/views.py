from django.contrib.auth.models import User
from rest_framework import viewsets

from .serializers import GameSerializer, UserSerializer, LocationSerializer
from AmazingRaceApp.models import Game, Location


class GameView(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by('title')
    serializer_class = GameSerializer

    # def get(self, request):


class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LocationView(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer