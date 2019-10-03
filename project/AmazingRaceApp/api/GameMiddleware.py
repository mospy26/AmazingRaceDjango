from django.contrib.auth.models import User 
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

import traceback

from ..models import Location, LocationUser, LocationGame, Game, GamePlayer

# API for the Location Database 
class GameMiddleware: 

    def __init__(self, game): 
        try: 
            self.locations = Location.objects.filter(game=game)
        except ObjectDoesNotExist: 
            print(traceback.print_exc())
        except EmptyResultSet: 
            print(traceback.print_exc())

        self.game_name = game
        self.locations = Location.object.filter(game=game).values()
        self.game_name = Game.object.filter(game=game).values()
    
    def get_all_players(self):
        game_players = GamePlayer.object.filter(game=self.game_name).values()

        for players in game_players: 
            pass 

