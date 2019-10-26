import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from django.utils.datetime_safe import datetime
import random

import traceback

from ..models import Game, GameCreator, Location
from .GameMiddleware import _GameMiddleware

""" 
This is an API for the following tasks:
    - for getting all Games and data of it that was created by a creator    
"""


class GameCreatorMiddleware:

    def __init__(self, username):

        try:
            self.user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            print(traceback.print_exc())
        except EmptyResultSet:
            print(traceback.print_exc())

        self.games = GameCreator.objects.filter(creator=self.user).select_related('game')
        self.game_middleware = None

    """
        Will return a generator of a list of games the current user has created.
        
        e.g. Getting the code of all games created by this user:
            ```
            g = GameCreatorMiddleWare(username=user)
            for game in created_games():
                print(g.code)
            ```
        Game contains:
            - code
            - archived (T/F)
            - live (T/F)
            - start_time
            - end_time
            - players
    """

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    # writing correct db query dont run query per user
    def created_games(self):
        for game in self.games:
            yield game.game

    def get_number_created_games(self):
        return len(self.games)

    def get_ordered_locations_of_game(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.ordered_locations()

    def get_location_at_x(self, code, x):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.get_x_location(x)

    def get_leaderboard(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.game_leaderboard()
    
    def get_status_of_game(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.get_status()
    def get_code_and_name(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.get_code_and_name()

    def update_location_order(self, location_codes_list, game_code):
        counter = 1
        game = Game.objects.get(code=game_code)
        for code in location_codes_list:
            location = Location.objects.get(code=code, game=game)
            if location.order != counter:
                location.order = counter
                location.save()
            counter += 1

    def is_authorized_to_access_game(self, code):
        return GameCreator.objects.filter(game=_GameMiddleware(code).game, creator=self.user).exists()
