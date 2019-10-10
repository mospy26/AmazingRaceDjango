import datetime

from django.db import models
from django.contrib.auth.models import User


# https://stackoverflow.com/questions/9498012/how-to-display-images-from-model-in-django
# REMEMBER TO MAKE MIGRATIONS and MIGRATE


class ProfilePictures(models.Model):
    picture = models.ImageField(upload_to="profile_picture", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Game(models.Model):
    title = models.CharField(max_length=50)
    archived = models.BooleanField()
    code = models.TextField(max_length=100, unique=True)
    live = models.BooleanField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    players = models.ManyToManyField(User)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        from AmazingRaceApp.api import GameCreatorMiddleware
        self = GameCreatorMiddleware.GameCreatorMiddleware._refactor_game_data(self)
        return super(Game, self).save()


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
    order = models.IntegerField()


class LocationUser(models.Model):
    time_visited = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class GamePlayer(models.Model):
    rank = models.BigIntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('game', 'player')
