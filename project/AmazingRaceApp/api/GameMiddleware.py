from django.contrib.auth.models import User
from django.db.models import Subquery
from django.utils.datetime_safe import datetime

from ..models import Location, Game, GamePlayer


# API for the Game Database
class _GameMiddleware:

    def __init__(self, code):
        self.game = Game.objects.get(code=code)
        self.locations = Location.objects.filter(game=self.game)
        self.game_players = GamePlayer.objects.filter(game=self.game).select_related('player').order_by('rank')
        self.users = User.objects.filter(id__in=Subquery(self.game_players.values('player')))

    def get_all_players(self):
        for user in self.users:
            yield user

    # returns tuple of rank and player name
    # note that player refers to an object encapsulating all data about him/her.
    # and game refers to an object encapsulating all data about the game (code, title etc.)
    # rank is an integer
    def game_leaderboard(self):
        for player in self.game_players:
            yield (player.rank, player.player.first_name + " " + player.player.last_name)

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
        for location in game_locations:
            yield location

    @classmethod
    def make_live(self, game: Game):
        # defines what happens when a game is made live
        game.live = True
        game.start_time = datetime.now()
        game.end_time = datetime.now()
        return game