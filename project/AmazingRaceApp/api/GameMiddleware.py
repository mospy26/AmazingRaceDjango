from django.contrib.auth.models import User
from django.db.models import Subquery

from ..models import Location, Game, GamePlayer


# API for the Game Database
class GameMiddleware:

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