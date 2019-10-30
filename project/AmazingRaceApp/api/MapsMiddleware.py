# https://www.youtube.com/watch?v=0IjdfgmWzMk&t=4s
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import geopy.geocoders
from geopy import distance
import certifi
import ssl
import re

import random
import string

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
        while True:
            try:
                n = self.nominatim.geocode(location_name + ', ' + city + ', ' + country)
                break
            except GeocoderTimedOut:
                return 50, 100
        return n.latitude, n.longitude

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
            latitude = float(latitude)
            longitude = float(longitude)

            yield (latitude, longitude, location.name)

    def get_all_name_code(self):
        location = Location.objects.all()
        i = 0
        for l in location:
            i += 1
            yield i, l.name, l.code

    def create_game_location(self, game_code, area_name, custom_name='', city='', country=''):
        if custom_name is None or custom_name == '':
            custom_name = area_name
        latitude, longitude = self.get_coordinate(area_name, city, country)

        location_code = self._generate_code(game_code)
        game = Game.objects.get(code=game_code)
        existing_locations = Location.objects.filter(game=game)

        order = 1 if not existing_locations.exists() else existing_locations.order_by('order').last().order + 1

        new_location = Location(name=custom_name,
                                clues="",
                                longitude=str(longitude),
                                latitude=str(latitude),
                                code=location_code,
                                game=game,
                                order=order)
        new_location.save()
        return new_location

    def _generate_code(self, game_code):
        location_codes = Location.objects.filter(game=Game.objects.get(code=game_code)).values_list('code')
        while True:
            unique = True
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            code = code[:4] + "-" + code[4:]
            for existing_code in location_codes:
                if code == existing_code:
                    unique = False
                    break
            if unique:
                return code

    def delete_location(self, game_code, location_code):
        game = Game.objects.get(code=game_code)
        location = Location.objects.filter(game=game_code, location_code=location_code)
        if (len(location) != 1):
            return 
        location[0].delete()
        return None

    def convert_degrees_to_string(self, string):
        degrees, minutes, seconds, direction = re.split('[°\'"]+', string)
        dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60);
        if direction == 'E' or direction == 'N':
            dd *= -1
        return float(dd)
