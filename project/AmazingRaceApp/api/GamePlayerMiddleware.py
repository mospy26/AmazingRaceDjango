from django.contrib.auth.models import User

import datetime

from AmazingRaceApp.api.GameMiddleware import _GameMiddleware
from ..models import GamePlayer, Game, Location, LocationUser, GameCreator


class GamePlayerMiddleware:

    def __init__(self, username):
        self.user = User.objects.get(username=username)
        self.games = Game.objects.filter(players=self.user)

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def get_games_played(self):
        return len(self.games)

    """
        Registers a player's visit to a location
    """
    def visit_location(self, location_code, game_code):
        game = Game.objects.get(code=game_code)
        game_locations = []
        locations_visited = []

        for x in LocationUser.objects.values_list('location_id').filter(user=self.user):
            locations_visited.append(Location.objects.get(id=x[0]).code)

        for x in Location.objects.values_list('code').filter(game=game).order_by('order'):
            game_locations.append(x[0])

        first = True
        for x in game_locations:
            if x not in locations_visited:
                if not first:
                    return False
                first = False
                if location_code == x:
                    current_location = LocationUser.objects.create(
                        time_visited=datetime.datetime.now(),
                        user=self.user,
                        location=Location.objects.get(code=location_code)
                    )
                    return True
        return False

    """
    Returns all the clue for all the games that are currently live for the player 
    """
    def retrieve_clue(self):
        for game in self.games:
            if game.live is False:
                continue
            locations = Location.objects.filter(game=game, locationuser__time_visited__lte=datetime.datetime.now())
            for location in locations:
                yield game.code, location.name, location.clues

    """
    Gets the cursor to the table which contains 
    all the locations have been visited by the user 
    along with the order, name, clue and code (if visited)
    else it returns ???
    """
    def locations_visited(self, game_code):
        game = Game.objects.get(code=game_code)
        all_locations = Location.objects.filter(game=game)

        first = True

        for this_location in all_locations:
            if LocationUser.objects.filter(location=this_location, user=self.user).exists():
                yield this_location.order, this_location.name, this_location.clues, this_location.code
            else:
                if first:
                    yield this_location.order, "???", this_location.clues, "???"
                    first = False
                else:
                    yield this_location.order, "???", "???", "???"

    """
    Gets the cursor to a list of games played 
    (live or past) by the user 
    """
    def list_played_games(self):
        for game in self.games:
            game_creator = GameCreator.objects.get(game=game)
            rank = GamePlayer.objects.get(game=game, player=self.user)
            yield game, game_creator.creator.username, rank.rank

    """
    Gets the cursor to the rank of the x recent games. The 
    x recent games prioritizes live games first AND then non live games.

    - Latest live games are prioritized off latest start time (since end time may be unknown)
    - Latest non live games are prioritized off latest end time
    """
    def rank_in_most_recent_games(self, x):
        # Prioritize live_games first 
        live_games = Game.objects.filter(players=self.user, live=True).order_by('-start_time')[:x]

        # Take the latest start time if possible
        x = x - len(live_games)
        non_live_games = []
        if x > 0:
            non_live_games = Game.objects.filter(players=self.user, live=False).order_by('-end_time')[:x]

        # Begin the games
        for games in live_games:
            for i in GamePlayer.objects.filter(game=games, player=self.user).values('rank'):
                yield games.title, i['rank'], games.start_time
        for games in non_live_games:
            for i in GamePlayer.objects.filter(game=games, player=self.user).values('rank'):
                yield games.title, i['rank'], games.start_time

    """
    Returns the number of games played for this user / number of locations in game
    """
    def num_games_played(self):
        return len(Game.objects.filter(players=self.user))

    """
    For a game, returns a pair where it is the number of locations visited to 
    number of locations in total for a game
    """
    def num_of_visited_locations_in_game(self, game_code):
        # Get the game object
        game = Game.objects.get(code=game_code)
        # Get the list of locations in the game 
        locations = Location.objects.filter(game=game)

        # Get the total number of locations 
        total_locations = len(locations)

        # Variable for number of locations visited 
        no_of_visited_locations = 0

        for i in locations:
            no_of_visited_locations += len(LocationUser.objects.filter(user=self.user, location=i))

        return no_of_visited_locations, total_locations

    def get_status_of_game(self, game_code):
        game = _GameMiddleware(game_code)
        return game.get_status()

    """
        Authorisation checks: checks if this user is authorised to view this game
    """
    def is_authorized_to_access_game(self, code):
        game = _GameMiddleware(code)
        if not game.game:
            return False
        return GamePlayer.objects.filter(game=_GameMiddleware(code).game, player=self.user).exists()

    """
        Checks if a this player can join this game (i.e. has not joined it, or it hasn't been archived yet)
    """
    def can_join_game(self, code):
        to_join_game = Game.objects.filter(code=code)

        if not to_join_game.exists():
            return False

        if to_join_game.archived:
            return False

        game_player = GamePlayer.objects.filter(game=to_join_game.first(), player=self.user)

        if game_player.exists():
            return False

        game_creator = GameCreator.objects.filter(game=to_join_game.first(), creator=self.user)
        if game_creator.exists():
            return False

        return True

    """
        Allows this user to join a game whose code is specified
    """
    def join_game(self, code):
        to_join_game = Game.objects.get(code=code)

        players = GamePlayer.objects.filter(game=to_join_game)
        rank = 0 if not players.exists() else players.order_by('-rank').first().rank + 1

        game_player = GamePlayer.objects.create(
            rank=rank,
            game=to_join_game,
            player=self.user
        )