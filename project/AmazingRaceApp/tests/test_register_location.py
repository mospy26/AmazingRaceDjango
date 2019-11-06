from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware

class TestRegisterLocation(DatabaseRequiredTests):

    def test_valid_location_code_of_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V4H7-GFEN', 'WS30-8FA3')
        self.assertTrue(result, "Error! User cannot add a valid game location of a joined game")

    def test_invalid_location_code_of_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V4H7-EEEN', 'WS30-8FA3')
        self.assertFalse(result, "Error! User can add an invalid game location of a joined game")

    def test_valid_location_code_of_created_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        #Canva location, Canva game
        result = user_middleware.visit_location('24Q9-72EG', '13T2-JFRN')
        self.assertFalse(result, "Error! User can add a game location of a created game")

    def test_valid__but_wrong_order_location_code_of_created_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        #Deloitte location, Canva game
        result = user_middleware.visit_location('4GL4-BHJ3', '13T2-JFRN')
        self.assertFalse(result, "Error! User can add an out of order game location of a created game")

    def test_invalid_location_code_of_created_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        #Canva location, Canva game
        result = user_middleware.visit_location('2QQQ-72EG', '13T2-JFRN')
        self.assertFalse(result, "Error! User can add an invalid game location of a created game")

    def test_valid_but_wrong_order_location_code_of_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('UFQ7-XMJO', 'WS30-8FA3')
        self.assertFalse(result, "Error! User can add a valid game location in the wrong order of a joined game")

    def test_valid_location_code_of_invalid_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V4H7-GFEN', 'W2Z0-8888')
        self.assertFalse(result, "Error! User can add a valid game location of an invalid game")

    def test_invalid_location_code_of_invalid_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V444-GFEN', 'W2Z0-8888')
        self.assertFalse(result, "Error! User cannot add a valid game location of a joined game")

    def test_valid_location_code_of_non_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        #Marine Drive Mumbai location in Jewel of India game
        result = user_middleware.visit_location('9V7D-2JZI', 'RIPM-VKBR')
        self.assertFalse(result, "Error! User can add a valid game location of a non-joined game")

    def test_valid_location_code_of_wrong_non_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('V4H7-GFEN', 'RIPM-VKBR')
        self.assertFalse(result, "Error! User cannot add a valid game location of a joined game")

    def test_invalid_location_code_of_non_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        result = user_middleware.visit_location('9999-GFEN', 'RIPM-VKBR')
        self.assertFalse(result, "Error! User can add a invalid game location of a mon-joined game")

    def test_valid_but_wrong_order_location_code_of_non_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        #Juhu Beach location of Jewel of India game
        result = user_middleware.visit_location('6VK7-IG74', 'RIPM-VKBR')
        self.assertFalse(result, "Error! User can add a valid game location of wrong order to a non-joined game")
