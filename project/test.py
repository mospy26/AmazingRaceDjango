'''
This file serves to debug the API classes/methods. Below is an example of 
how to write such code 
'''

# # To run, the command is "python manage.py shell < test.py"
#
# from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware
# from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware
#
# g = MapsMiddleware()
# g.get_coordinate('Central Park', 'Sydney', 'Australia')
# #variable = g.get_distance("Auburn Sydney", "Perth")
# # variable = g.get_coordinate("PNR, Sydney")
# #print(variable)
#
# p = g.get_list_of_long_lat("NZSL-JWBK")
# for ob in p:
#     print(ob)
from django.contrib.auth.models import User

from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware
from AmazingRaceApp.models import Game

player = GamePlayerMiddleware('echa')
for rank in player.rank_in_most_recent_games(10):
    print(rank[0])