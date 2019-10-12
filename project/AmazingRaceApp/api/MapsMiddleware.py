# https://www.youtube.com/watch?v=0IjdfgmWzMk&t=4s

from geopy.geocoders import Nominatim
from geopy import distance

from ..models import ProfilePictures, GamePlayer, Game, Location, LocationUser

class MapsMiddleware: 

    def __init__(self): 
        self.nominatim = Nominatim() 

    '''
    Returns the (latitude, longitude) tuples
    '''
    def get_coordinate(self, location):
        n = self.nominatim.geocode(location)
        return (n.latitude, n.longitude) 

    '''
    Returns the distance from the origin to destination in Kilometers
    '''
    def get_distance(self, origin, destination): 
        origin = self.get_coordinate(origin)
        destination = self.get_coordinate(destination)
        return distance.distance(origin, destination).km

    '''
    Returns a list of locations for a given game_code with it's corresponding
    latitude and longitude
    '''
    def get_list_of_long_lat(self, game_code):
        game = Game.objects.get(code=game_code)
        all_locations = Location.objects.filter(game=game)

        for location in all_locations: 
            latitude, longitude = self.get_coordinate(location.name)
            yield location.name, latitude, longitude
    