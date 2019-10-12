'''
This file serves to debug the API classes/methods. Below is an example of 
how to write such code 
'''

# To run, the command is "python manage.py shell < test.py"

from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware

g = MapsMiddleware()

lol = g.get_distance("Sydney Opera House", "The University Of Sydney")
print(lol)