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
        location_exists = Location.objects.filter(game=game, name="Rotorua").exists()
        self.assertTrue(location_exists, "Location failed to save")

    def test_location_should_not_save_in_database(self):
        game_code = "AAAA-AAAA"
        result = None
        try:
            result = self.maps.create_game_location(game_code=game_code, area_name="Rotorua", city='Rotorua',
                                                    country='New Zealand')
        except:
            # should be an exception in finding the game
            self.assertTrue(True)
            return
        self.assertFalse(result is not None, "ERROR! The game locations must not be saved for an incorrect game")

    def test_location_order_is_correct(self):
        # Jacinda Arden - Australia
        game_code = "664P-RLCG"
        new_location = self.maps.create_game_location(game_code=game_code, area_name="Rotorua", city='Rotorua',
                                                      country='New Zealand')
        game = Game.objects.get(code=game_code)
        len_locations = len(Location.objects.filter(game=game))
        self.assertEquals(len_locations, new_location.order, "Location order is not correct")

    def test_should_not_add_location_to_game_not_owned_by_user(self):
        game_creator = GameCreatorMiddleware(self.david.username)

        # Calvin's game 
        calvins_game_code = "4Y1H-M4NX"
        self.assertFalse(game_creator.is_authorized_to_access_game(calvins_game_code), "ERROR! Can add locations to a "
                                                                                       "game not owned by a user!")

    def test_cannot_add_location_to_an_archived_game(self):
        game_code = "9XMQ-FXYJ"
        game_creator_middleware = GameCreatorMiddleware(self.david.username)
        game_creator_middleware.stop_game(game_code)

        # if can_change_game(code) is false, no changes are allowed to the game, even adding location is not allowed
        self.assertFalse(game_creator_middleware.can_change_game(game_code), "ERROR! Can add location to a game even "
                                                                             "after it is archived")

    def test_cannot_add_location_to_a_live_game(self):
        # David's game
        live_game_code = "9XMQ-FXYJ"

        game_creator_middleware = GameCreatorMiddleware(self.david.username)
        game_creator_middleware.stop_game(live_game_code)

        # if can_change_game(code) is false, no changes are allowed to the game, even adding locations are not allowed
        self.assertFalse(game_creator_middleware.can_change_game(live_game_code),
                         "ERROR! Can add location to a game even "
                         "after it is live")

    def test_can_add_location_to_published_game_of_yours(self):
        unpublished_game_code = "13T2-JFRN"

        game_creator_middleware = GameCreatorMiddleware(self.david.username)

        # if can_change_game(code) is True, changes are allowed to the game, including adding locations
        self.assertTrue(game_creator_middleware.can_change_game(unpublished_game_code),
                        "ERROR! Cannot add location to a game even "
                        "if its not published yet")
