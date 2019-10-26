import random
import string

from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.db import models
from django.contrib.auth.models import User


# REMEMBER TO MAKE MIGRATIONS and MIGRATE

class ProfilePictures(models.Model):
    picture = models.ImageField(upload_to="profile_picture", default="/profile_picture/default-picture.png", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Game(models.Model):
    title = models.CharField(max_length=50)
    archived = models.BooleanField(default=False)
    code = models.TextField(max_length=100, unique=True)
    live = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    players = models.ManyToManyField(User)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.start_time and self.end_time:
            self._refactor_input()
        if self.code == "":
            self._generate_code()
        return super(Game, self).save()

    def _generate_code(self):
        game_codes = Game.objects.values_list('code')
        while True:
            game_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            game_code = game_code[:4] + "-" + game_code[4:]
            for existing_code in game_codes:
                if game_code == existing_code:
                    break
                self.code = game_code
                return

    def _refactor_input(self):

        if self.end_time <= self.start_time:
            self.end_time = None
            self.start_time = None
            self.live = False
            self.archived = False

        elif self.end_time is not None and self.end_time <= timezone.now():
            self.live = False
            self.archived = True

        elif self.start_time is None or self.end_time is None:
            self.live = False
            self.live = False

        else:
            self.live = True
            self.archived = False


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.code == "":
            self._generate_code()
        return super(Location, self).save()

    def _generate_code(self):
        location_codes = Location.objects.filter(game=self.game).values_list('code')
        while True:
            location_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            location_code = location_code[:4] + "-" + location_code[4:]
            if len(location_codes) == 0:
                self.code = location_code
                return
            for existing_code in location_codes:
                if location_code == existing_code:
                    break
                self.code = location_code
                return

    def _generate_latitude_and_longitute(self):
        pass


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
