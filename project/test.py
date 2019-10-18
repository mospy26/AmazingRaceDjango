'''
This file serves to debug the API classes/methods. Below is an example of 
how to write such code 
'''

# To run, the command is "python manage.py shell < test.py"

from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware

g = MapsMiddleware()
g.get_coordinate('Sydney')
# variable = g.get_distance("Sydney Opera House", "The University Of Sydney")
variable = g.get_coordinate("University Of Sydney")
print(variable)