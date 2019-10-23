# https://www.youtube.com/watch?v=0IjdfgmWzMk&t=4s

from geopy.geocoders import Nominatim
import geopy.geocoders
from geopy import distance
import certifi
import ssl

from ..models import ProfilePictures, GamePlayer, Game, Location, LocationUser


class MapsMiddleware:

    def __init__(self):
        ctx = ssl.create_default_context(cafile=certifi.where())
        geopy.geocoders.options.default_ssl_context = ctx
        self.nominatim = Nominatim(user_agent='myapplication', scheme='http')

    '''
    Returns the (latitude, longitude) tuples
    '''

    def get_coordinate(self, location_name, city='', country=''):
        n = self.nominatim.geocode(location_name + ', ' + city + ', ' + country)
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
    
    def _convert_to_decimal(self, degrees):
        total = 0
        degrees = degrees.split("˚")
        total = total + float(degrees[0])
        degrees = degrees[1].split("'")
        total = total + float(degrees[0])/60
        degrees = degrees[1].split("\"")
        total = total + float(degrees[0])/3600
        
        return total

    def get_list_of_long_lat(self, game_code):
        game = Game.objects.get(code=game_code)
        all_locations = Location.objects.filter(game=game)

        for location in all_locations:
            latitude, longitude = self.get_coordinate(location.name)
            latitude = self._convert_to_decimal(latitude)
            longitude = self._convert_to_decimal(longitude)
            
            yield (location.name, latitude, longitude)

    def get_all_name_code(self):
        location = Location.objects.all()
        i = 0
        for l in location:
            i += 1
            yield i, l.name, l.code
