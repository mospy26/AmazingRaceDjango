from ..models import Location, LocationUser, LocationGame

# API for the Location Database 
class LocationMiddleware: 

    def __init__(self): 
        pass 

    # Returns a list of location name
    @classmethod
    def get_all_locations(cls, game): 
        return Location.objects.values('name', game=game)
    
    # Returns the game associated with the location 
    @classmethod
    def get_game(cls, location):
        return Location.objects.values('game', location=location)

    # Returns the clues associated with the location 
    @classmethod
    def get_clues(cls, location): 
        return Location.objects.values('clues', location=location)
    
    @classmethod
    def get_longitude(cls, location): 
        return Location.objects.values('longitude', location=location)
    
    @classmethod
    def get_latitude(cls, location): 
        return Location.objects.values('latitude', location=location)

    @classmethod
    def get_users_in_location(cls, location): 
        return LocationUser.objects.filter(location=location) 
    
