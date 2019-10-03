from django.db import models
from django.contrib.auth.models import User


# https://stackoverflow.com/questions/9498012/how-to-display-images-from-model-in-django
class ProfilePictures(models.Model):
    picture = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Game(models.Model):
    archived = models.BooleanField()
    code = models.TextField(max_length=100)
    live = models.BooleanField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    players = models.ManyToManyField(User)


class GameCreator(models.Model):
    game = models.OneToOneField(Game, primary_key=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Location(models.Model):
    name = models.TextField()
    clues = models.TextField()
    longitude = models.TextField()
    latitude = models.TextField()
    code = models.TextField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class LocationUser(models.Model):
    time_visited = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class LocationGame(models.Model):
    location_order = models.TextField(max_length=300)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('location_order', 'game')


class GamePlayer(models.Model):
    rank = models.BigIntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('game', 'player')
