from django.contrib.auth.models import User

from ..models import Game, GameCreator, Location
from .GameMiddleware import _GameMiddleware

""" 
This is an API for the following tasks:
    - for getting all Games and data of it that was created by a creator    
"""


class GameCreatorMiddleware:

    def __init__(self, username):

        self.user = None if not username else User.objects.get(username=username)

        self.games = GameCreator.objects.filter(creator=self.user).select_related('game')
        self.game_middleware = None


    def delete_game(self, code):
        self.game_middleware = _GameMiddleware(code)
        self.game_middleware.delete_game()

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    """
        Will return a generator of a list of games the current user has created.
    """
    def created_games(self):
        for game in self.games:
            yield game.game

    def get_number_created_games(self):
        return len(self.games)

    """
        Will return a generator of ordered locations of game with specified code
    """
    def get_ordered_locations_of_game(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.ordered_locations()

    """
        Will return the location that has the specified code
    """
    def get_location_by_code(self, code):
        location = Location.objects.filter(code=code)
        return None if not location.exists() else location

    def get_location_at_x(self, code, x):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.get_x_location(x)

    """
        Will return leaderboard of a game
    """
    def get_leaderboard(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.game_leaderboard()

    """
        Will return the status of a game
    """
    def get_status_of_game(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.get_status()

    def get_code_and_name(self, code):
        self.game_middleware = _GameMiddleware(code)
        return self.game_middleware.get_code_and_name()

    """
        Will update the location order of a game whose code is specified
    """
    def update_location_order(self, location_codes_list, game_code):
        counter = 1
        game = Game.objects.get(code=game_code)
        for code in location_codes_list:
            location = Location.objects.get(code=code, game=game)
            if location.order != counter:
                location.order = counter
                location.save()
            counter += 1

    """
        Security Authorisation check: Will check if a game is accessbile to this user
    """
    def is_authorized_to_access_game(self, code):
        game = _GameMiddleware(code)
        if not game.game:
            return False
        return GameCreator.objects.filter(game=_GameMiddleware(code).game, creator=self.user).exists()

    def get_game(self, code):
        if self.is_authorized_to_access_game(code):
            game = _GameMiddleware(code)
            return game

    def is_live_game(self, code):
        return _GameMiddleware(code).game.live

    """
        Will start the game whose code is specified
    """
    def start_game(self, code):
        self.game_middleware = _GameMiddleware(code)
        self.game_middleware.make_live()

    """
        Will stop the game whose code is specified
    """
    def stop_game(self, code):
        self.game_middleware = _GameMiddleware(code)
        self.game_middleware.end_game()

    """
        Will return location of a game both of whose codes are specified
    """
    def get_location_of_game(self, game_code, location_code):
        if not self.is_authorized_to_access_game(game_code):
            return None
        game = _GameMiddleware(game_code)
        if not game.game:
            return None
        return game.get_location(location_code)
