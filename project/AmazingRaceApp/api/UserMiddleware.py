from ..models import ProfilePictures, GameCreator, GamePlayer, Game

# API for getting all locations in a game 
class UserMiddleware: 

    def __init__(self): 
        pass 

    # TODO: # https://stackoverflow.com/questions/9498012/how-to-display-images-from-model-in-django
    @classmethod
    def getProfilePicture(cls, user): 
        return ProfilePictures.objects.filter(user=user)

    # Returns all the games created by the user 
    @classmethod
    def getAllGamesCreated(cls, user): 
        return GameCreator.objects.filter(creator=user)

    # Returns all the games that the user is participating
    @classmethod
    def getAllGamesParticipating(cls, user): 
        return GamePlayer.objects.values('game', player=user)
    
    # Returns the ranks, correspondent to the game of a user 
    @classmethod
    def getRankOfPlayer(cls, user): 
        return GamePlayer.objects.values('game', 'rank', player=user)