from django.contrib import admin
from .models import ProfilePictures, Game, GameCreator, GamePlayer, \
    Location, LocationGame, LocationUser

# Register your models here.

admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(GameCreator)
admin.site.register(LocationUser)
admin.site.register(Location)
admin.site.register(LocationGame)
admin.site.register(ProfilePictures)