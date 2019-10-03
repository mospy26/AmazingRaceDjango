from django.contrib.auth.models import User 
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

import traceback 

from ..models import ProfilePictures, GamePlayer, Game


# API for getting all locations in a game 
class GamePlayerMiddleware: 

    def __init__(self, username):         
        try: 
            self.user = User.objects.get(username=user)
        except ObjectDoesNotExist:
            print(traceback.print_exc())
        except EmptyResultSet: 
            print(traceback.print_exc())

        self.games = GamePlayer.objects.filter(players=username).values()
        # TODO: # https://stackoverflow.com/questions/9498012/how-to-display-images-from-model-in-django
        self.profile_picture = ProfilePictures.objects.filter(user=username).get()

    def get_profile_picture(self): 
        return self.profile_picture

    # Returns all the games that the user is participating in 
    def get_all_games_participating(self): 
        games = GamePlayer.objects.filter(player=user).values('game')
        for game in games: 
            yield Game.objects.get(pk=games['game_id'])
    
    # Returns the ranks, correspondent to the game of a user 
    def get_rank_of_player(self): 
        games_rank = GamePlayer.objects.filter(player=user).values('game', 'rank')
        for game in games_rank: 
            pass 