'''
This file serves to debug the API classes/methods. Below is an example of 
how to write such code 
'''

# To run, the command is "python manage.py shell < test.py"

from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware

import os 

# Example on how to use Update and Get Profile Pictures: 
g = GamePlayerMiddleware("blam")

# Must get the absolute path of the picture (Windows user be aware of your terminal like shown below)
# Note the file is saved under Project/project/media/profile_picture
g.update_profile_pictures("/mnt/c/Users/Markl/Desktop/picture.png")
print(g.get_profile_picture())
# g.delete_profile_picture()
