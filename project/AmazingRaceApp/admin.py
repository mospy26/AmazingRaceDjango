from django.contrib import admin
from .models import Game, GameCreator, GamePlayer, \
    Location, LocationUser

admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(GameCreator)
admin.site.register(LocationUser)
admin.site.register(Location)
