from ..models import Location, LocationUser, LocationGame

# API for the Location Database 
class LocationMiddleware: 

    def __init__(self): 
        pass 

    # Returns a list of location name
    @classmethod
    def getAllLocations(cls, game): 
        return Location.objects.values('name', game=game)
    
    # Returns the game associated with the location 
    @classmethod
    def getGame(cls, location):
        return Location.objects.values('game', location=location)

    # Returns the clues associated with the location 
    @classmethod
    def getClues(cls, location): 
        return Location.objects.values('clues', location=location)
    
    @classmethod
    def getLongitude(cls, location): 
        return Location.objects.values('longitude', location=location)
    
    @classmethod
    def getLatitude(cls, location): 
        return Location.objects.values('latitude', location=location)

    @classmethod
    def getUsersInLocation(cls, location): 
        return LocationUser.objects.filter(location=location) 
    
