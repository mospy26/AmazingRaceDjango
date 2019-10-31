from django.contrib.auth.models import User
from django.db.models import Subquery
from django.utils.datetime_safe import datetime

from ..models import Location, Game, GamePlayer


# API for the Game Model
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
        for player in self.game_players:
            yield player.rank, player.player.username

    """
        Gives the ordered locations of a game in sequence
    """

    def ordered_locations(self):
        game_locations = Location.objects.filter(game=self.game).order_by('order')
        for location in game_locations:
            yield location.order, location

    def get_x_location(self, x):
        game_locations = Location.objects.filter(game=self.game).order_by('order')
        for location in game_locations:
            yield location

    """
        Changes a game name
    """

    def change_name(self, name):
        self.game.title = name
        self.game.save()

    """
        Makes a game live
    """

    def make_live(self):
        # defines what happens when a game is made live
        self.game.live = True
        self.game.start_time = datetime.now()
        self.game.end_time = None
        return self.game.save()

    """
        Return a string status
            Live means game has started and not ended yet
            Closed means game was stopped and hence archived
            Not Published means game has not been started ever
    """

    def get_status(self):
        if self.game.live:
            return "Live"
        elif self.game.archived:
            return "Closed"
        else:
            return "Not Published"

    """
        Ends a game i.e. archives it
    """

    def end_game(self):
        self.game.live = False
        self.game.archived = True
        self.game.end_time = datetime.now()
        return self.game.save()

    def get_location(self, code):
        location = Location.objects.filter(code=code)
        return None if not location.exists() else location.first()
