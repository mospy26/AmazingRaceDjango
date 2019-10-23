from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from django.core.files import File

import traceback
import os
from ..models import ProfilePictures, GamePlayer, Game, Location, LocationUser, GameCreator


# API for getting all locations in a game 
class GamePlayerMiddleware:

    def __init__(self, username):
        self.user = User.objects.get(username=username)
        self.games = Game.objects.filter(players=self.user)
        self.profilePic = None if not ProfilePictures.objects.filter(user=self.user).exists() else \
            ProfilePictures.objects.get(user=self.user)

    '''
    Source: 
    - https://www.revsys.com/tidbits/loading-django-files-from-code/
    - https://www.youtube.com/watch?v=1jxVzOnIqyI
    - https://stackoverflow.com/questions/9498012/how-to-display-images-from-model-in-django

    Updates the profile picture by first deleting the profile picture and then 
    uploading the picture 

    @param: The Absolute path for the image
    @return: Nothing
    '''

    def update_profile_pictures(self, image_url):
        if self.profilePic:
            self.profilePic.picture.delete(save=True)
        django_file = File(open(image_url, "rb"))
        self.profilePic.picture.save(self.user.username + "-profile-pic" + ".jpeg", django_file, save=True)

    def delete_profile_picture(self):
        self.profilePic.picture.delete(save=True)

    # TODO: Check if this actually renders when called on the front end 
    def get_profile_picture(self):
        profile_pic = self.profilePic.picture.url
        exists = os.path.exists("../" + profile_pic)
        
        if not profile_pic or not exists:
            return "/media/profile_picture/default-picture.png" 
        
        return profile_pic

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def get_games_played(self):
        return len(self.games);

    '''
    Returns all the clue for all the games that are currently live for the player 

    @param: None
    @return: Returns a 3 item tuple corresponding in order: Game Code, Location name, Location Clue
    '''

    def retrieve_clue(self):
        for game in self.games:
            if game.live is False:
                continue
            locations = Location.objects.filter(game=game, locationuser__time_visited__lte=datetime.now())
            for location in locations:
                yield game.code, location.name, location.clues

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
        for game in self.games:
            game_creator = GameCreator.objects.get(game=game)
            rank = GamePlayer.objects.get(game=game, player=self.user)
            yield game, game_creator.creator.username, rank.rank

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
        if x > 0:
            non_live_games = Game.objects.filter(players=self.user, live=False).order_by('-end_time')[:x]

        # Begin the games
        for games in live_games:
            for i in GamePlayer.objects.filter(game=games, player=self.user).values('rank'):
                yield games.title, i['rank'], games.start_time.strftime('%d/%m/%Y')
        for games in non_live_games:
            for i in GamePlayer.objects.filter(game=games, player=self.user).values('rank'):
                yield games.title, i['rank'], games.start_time

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
