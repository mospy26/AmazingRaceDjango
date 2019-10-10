import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from django.utils.datetime_safe import datetime
import random

import traceback

from ..models import Game, GameCreator

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

    def created_games(self):
        for game in self.games:
            yield game.game

    """
    Will generate a code and prefil start and end times with default values and refactors live = False etc.
    """

    @classmethod
    def _refactor_game_data(self, game: Game):

        # Validation
        if game.end_time <= game.start_time:
            # return some error message
            # for now will reset both to a default value
            game.end_time = datetime(2000, 1, 2)
            game.start_time = datetime(2000, 1, 1)
            game.live = False
            game.archived = True

        elif game.end_time is not None and game.end_time <= datetime.now() and (game.live is True or game.archived is True):
            game.live = False
            game.archived = True

        if game.start_time is None:
            game.end_time = datetime(2000, 1, 2)
            game.start_time = datetime(2000, 1, 1)
            game.live = False
            game.archived = True

        game_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        game_code = game_code[:4] + "-" + game_code[4:]

        game.code = game_code

        return game
