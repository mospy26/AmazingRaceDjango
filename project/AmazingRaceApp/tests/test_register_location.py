import AmazingRaceApp.models
from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware


class TestRegisterLocation(DatabaseRequiredTests):

    def test_non_conventional_location_code_of_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('Non conventional code format....', 'WS30-8FA3')
        self.assertFalse(result, "ERROR! User can add a invalid game location code format of a joined game")

    def test_valid_location_code_of_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V4H7-GFEN', 'WS30-8FA3')
        self.assertTrue(result, "ERROR! User cannot add a valid game location of a joined game")

    def test_invalid_location_code_of_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V4H7-EEEN', 'WS30-8FA3')
        self.assertFalse(result, "ERROR! User can add an invalid game location of a joined game")

    def test_valid_location_code_of_not_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        # Canva location, Canva game

        game_code = '13T2-JFRN'
        # we know that if this fails, the post request won't work and hence this must be tested
        self.assertFalse(user_middleware.is_authorized_to_access_game(game_code),  "ERROR! User can register a game "
                                                                                     "location of a non-joined game")

    def test_valid_but_wrong_order_location_code_of_created_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        # Deloitte location, Canva game
        result = user_middleware.visit_location('4GL4-BHJ3', '13T2-JFRN')
        self.assertFalse(result, "ERROR! User can add an out of order game location of a created game")

    def test_valid_but_wrong_order_location_code_of_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('UFQ7-XMJO', 'WS30-8FA3')
        self.assertFalse(result, "ERROR! User can add a valid game location in the wrong order of a joined game")

    def test_valid_location_code_of_invalid_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)

        try:
            result = user_middleware.visit_location('V4H7-GFEN', 'W2Z0-8888')  # Invalid game but valid location codes
        except Exception as e:
            self.assertTrue(e.__class__ == AmazingRaceApp.models.Game.DoesNotExist, "ERROR! User cannot add an invalid "
                                                                                    "game location of a an invalud game")
            return

        self.assertFalse(True, "ERROR! User can add a valid game location of an invalid game")

    def test_invalid_location_code_of_invalid_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        try:
            result = user_middleware.visit_location('V444-GFEN', 'W2Z0-8888')  # Invalid game and location codes
        except Exception as e:
            self.assertTrue(e.__class__ == AmazingRaceApp.models.Game.DoesNotExist, "ERROR! User cannot add an invalid "
                                                                                    "game location of a an invalud game")
            return

        self.assertFalse(True, "ERROR! Invalid game is somehow validated...")

    def test_valid_location_code_of_wrong_non_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V4H7-GFEN', 'RIPM-VKBR')
        self.assertFalse(result, "ERROR! User cannot add a valid game location of a joined game")

    def test_invalid_location_code_of_non_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('9999-GFEN', 'RIPM-VKBR')
        self.assertFalse(result, "ERROR! User can add a invalid game location of a mon-joined game")

    def test_valid_but_wrong_order_location_code_of_non_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        # Juhu Beach location of Jewel of India game
        result = user_middleware.visit_location('6VK7-IG74', 'RIPM-VKBR')
        self.assertFalse(result, "ERROR! User can add a valid game location of wrong order to a non-joined game")
