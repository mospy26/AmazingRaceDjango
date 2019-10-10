from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

import traceback

from ..models import GameCreator

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