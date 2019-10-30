import string

from django.contrib.auth.models import User
from django.db.models import Subquery
from django.utils.datetime_safe import datetime
import random
from ..models import Location, Game, GamePlayer


# API for the Game Database
class _GameMiddleware:

    def __init__(self, code):

        game = Game.objects.filter(code=code)
        self.game = None if not game.exists() else game.first()

        self.locations = Location.objects.filter(game=self.game)
        self.game_players = GamePlayer.objects.filter(game=self.game).select_related('player').order_by('rank')
        self.users = User.objects.filter(id__in=Subquery(self.game_players.values('player')))

    def get_all_players(self):
        for user in self.users:
            yield user

    def get_code_and_name(self):
        yield self.game.title, self.game.code

    '''
    Deletes the game from the database. When deleted, make sure to make the API object equate to this function 
    e.g.
    api = GameMiddleware(...)
    api = api.delete_game()

    @param None 
    @returns None to delete the API 
    '''
    def delete_game(self):
        self.game.delete()
        return None

    # returns tuple of rank and player name
    # note that player refers to an object encapsulating all data about him/her.
    # and game refers to an object encapsulating all data about the game (code, title etc.)
    # rank is an integer
    def game_leaderboard(self):
        i = 100  # TEMPORARY SUB FOR SCORE!
        for player in self.game_players:
            yield player.rank, i, player.player.username
            i = i - 1

    """
        Gives the entire location object, you will need to use attributes such as:
            - name
            - clues
            - longitude
            - latitude
            - code
            - game
            - order
    """

    def ordered_locations(self):
        game_locations = Location.objects.filter(game=self.game).order_by('order')
        i = 0
        for location in game_locations:
            i += 1
            yield i, location

    def get_x_location(self, x):
        game_locations = Location.objects.filter(game=self.game).order_by('order')
        i = 0
        for location in game_locations:
            yield location

    def change_name(self, name):
        self.game.title = name
        self.game.save()

    def make_live(self, game: Game):
        # defines what happens when a game is made live
        game.live = True
        game.start_time = datetime.now()
        game.end_time = datetime.now()
        return game

    def get_status(self):
        if self.game.live:
            return "Live"
        elif self.game.archived:
            return "Closed"
        else:
            return "Not Published"
