from django.contrib.auth.models import User 
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

import traceback 

from ..models import ProfilePictures, GamePlayer, Game, Location, LocationUser, LocationGame


# API for getting all locations in a game 
class GamePlayerMiddleware: 

    def __init__(self, username):         
<<<<<<< HEAD
        try: 
            self.user = User.objects.get(username=username)
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
        games = GamePlayer.objects.filter(player=self.user).values('game')
=======
        self.user = User.objects.get(username=username)

    # TODO
    def update_profile_pictures(self):
        pass 

    # TODO
    def get_profile_pictures(self):
        pass
    
    '''
    Returns all the clue for all the games that are currently live for the player 

    @param: None
    @return: Returns a 3 item tuple corresponding in order: Game Code, Location name, Location Clue
    '''
    def retrieve_clue(self):
        games = Game.objects.filter(live=True, players=self.user)
        
>>>>>>> backend_api_brendon
        for game in games: 
            locations = Location.objects.filter(game=game)
            for location in locations:
                yield game.code, location.name, location.clues
    
<<<<<<< HEAD
    # Returns the ranks, correspondent to the game of a user 
    def get_rank_of_player(self): 
        games_rank = GamePlayer.objects.filter(player=self.user).values('game', 'rank')
        for game in games_rank: 
            pass 
=======
    '''
    Gets the cursor to the table which contains 
    all the locations have been visited by the user 
    @param: None 
    @return: list of visited locations from the user 
    '''
    def locations_visited(self, game_code):
        game = Game.objects.get(code=game_code)
        all_locations = Location.objects.filter(game=game)

        for this_location in all_locations:
            if (LocationUser.objects.filter(location=this_location, user=self.user)):
                yield this_location.name                

    '''
    Gets the cursor to a list of games played 
    (live or past) by the user 
    @param: None 
    @return: list of games (by code) played by the user (live/past)
    '''
    def list_played_games(self):
        games = Game.objects.filter(players=self.user)
        for game in games: 
            yield game.code

    '''
    Gets the cursor to the rank of the x recent games. The 
    x recent games prioritizes live games first AND then non live games.

    - Latest live games are prioritized off latest start time (since end time may be unknown)
    - Latest non live games are prioritized off latest end time

    @param: x being the offset of recent games 
    @return: A Generator which yields a tuple (<Game Code>, <rank>) 
    '''
    def rank_in_most_recent_games(self, x):
        # Prioritize live_games first 
        live_games = Game.objects.filter(players=self.user, live=True).order_by('-start_time')[:x]
        # Take the latest start time if possible
        x = x - len(live_games)        
        non_live_games = []
        if (x > 0): 
            non_live_games = Game.objects.filter(players=self.user, live=False).order_by('-end_time')[:x]
        # Begin the games 
        for games in live_games:
            for i in GamePlayer.objects.filter(game=games, player=self.user).values('rank'):
                yield games.code, i['rank']
        for games in non_live_games: 
            for i in GamePlayer.objects.filter(game=games, player=self.user).values('rank'):
                yield games.code, i['rank'] 

    '''
    Returns the number of games played for this user / number of locations in game

    @param: None
    @return: number of games played for this user to total number of locations in game  
    '''
    def num_games_played(self):
        return len(Game.objects.filter(players=self.user)) 

    '''
    For a game, returns a pair where it is the number of locations visited to 
    number of locations in total for a game

    @param: The game code 
    @return: A pair of values where the first element is number of visited locations
            and second value is the number of locations in total for a game  
    '''
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
        
>>>>>>> backend_api_brendon