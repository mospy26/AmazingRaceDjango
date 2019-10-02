from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

import traceback

from ..models import GameCreator


""" 
This is an API for the following tasks:
    - for getting all Games and data of it that was created by a creator
    -
"""


class GameCreatorMiddleware:

    def __init__(self, username, current_game=None):

        try:
            self.user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            print(traceback.print_exc())
        except EmptyResultSet:
            print(traceback.print_exc())

        self.games = GameCreator.objects.filter()
        self.current_game = current_game if current_game is None else GameCreator.objects.filter(creator=current_game)

    def get_created_games(self):
        return GameCreator.objects.filter(creator=self.user)