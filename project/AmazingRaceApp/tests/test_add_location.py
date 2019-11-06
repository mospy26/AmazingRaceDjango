# Create_Game_Location - MapsMiddleware
from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware
from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests
from AmazingRaceApp.models import Location, Game, User
from AmazingRaceApp import models
from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware


class AddLocationTest(DatabaseRequiredTests):
    
    def setUp(self):
        super(AddLocationTest, self).setUp()
        self.maps = MapsMiddleware()

    def test_location_saves_correctly_in_database(self):
        # Jacinda Arden - Australia
        game_code = "664P-RLCG"
        self.maps.create_game_location(game_code=game_code, area_name="Rotorua", city='Rotorua', country='New Zealand') 
        game = Game.objects.get(code=game_code)
        locationExists = Location.objects.filter(game=game, name="Rotorua").exists()
        self.assertTrue(locationExists, "Location failed to save")

    def test_location_should_not_save_in_database(self):
        game_code = "AAAA-AAAA"
        result = None
        try: 
            result = self.maps.create_game_location(game_code=game_code, area_name="Rotorua", city='Rotorua', country='New Zealand')
        except:
            self.assertTrue(True)
            return
        self.assertFalse(result is not None, "ERROR! The game locations must not be saved for an incorrect game") 

    def test_location_order_is_correct(self):
        # Jacinda Arden - Australia
        game_code = "664P-RLCG"
        new_location = self.maps.create_game_location(game_code=game_code, area_name="Rotorua", city='Rotorua', country='New Zealand') 
        game = Game.objects.get(code=game_code)
        len_locations = len(Location.objects.filter(game=game))
        self.assertEquals(len_locations, new_location.order, "Location order is not correct")

    # -----------------THE BELOW CODE WE HAVEN'T ENFORCED/IMPLEMENTED--------------------------------
    def test_should_not_add_location_to_game_not_owned_by_user(self):
        game_creator = GameCreatorMiddleware(self.david.username)
        
        # Calvin's game 
        game = Game.objects.get(code = "4Y1H-M4NX")
        list_of_location_code = Location.objects.filter(game=game).values('code')

        try:         
            result = game_creator.update_location_order(game_code=game_code, locations_code_list=list_of_location_code)
        except:
            self.assertTrue(True)
            return
        self.fail()

    def cannot_add_location_to_an_archived_game(self):
        game_code = "4HNT-YR9O"
        result = None
        try: 
            result = self.maps.create_game_location(game_code=game_code, area_name="Rotorua", city='Rotorua', country='New Zealand')
        except:
            self.assertTrue(True)
            return
        self.assertFalse(result is not None, "ERROR! The location cannot be saved in an archived game")   


    def cannot_add_location_to_a_live_game(self):
        # Calvin's game
        live_game_code = "WS30-8FA3"

        try: 
            result = self.maps.create_game_location(game_code=live_game_code,  area_name="Rotorua", city='Rotorua', country='New Zealand')
        except: 
            self.assertTrue(True)
            return
        self.assertFalse(result is not None, "ERROR! The location cannot be saved in an archived game")   

    def can_add_location_to_published_game_of_yours(self):
        pass 
