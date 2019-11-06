from django.contrib.auth.models import User
from django.test import TestCase
from AmazingRaceApp.models import GameCreator, Game
from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware
from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware

class TestJoinGame(DatabaseRequiredTests):
    def test_user_cannot_join_a_not_published_game_of_another_creator(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        self.assertFalse(user_middleware.can_join_game("4Y1H-M4NX"), "Error! User can join a game that has not been published yet!")

    def test_user_can_join_live_game_they_are_not_in_of_another_creator(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        self.assertTrue(user_middleware.can_join_game("RIPM-VKBR"), "Error! User cannot join a live game they are not in!")

    def test_user_cannot_join_an_already_joined_game(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        self.assertFalse(user_middleware.can_join_game("WS30-8FA3"), "Error! User joined a game they are already in!")

    def test_user_cannot_join_archived_game_of_another_creator(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        game_creator_middleware = GameCreatorMiddleware(self.mustafa.username)
        game_creator_middleware.stop_game("RIPM-VKBR")
        self.assertFalse(user_middleware.can_join_game("RIPM-VKBR"), "Error! User joined an archived game!")

    def test_user_cannot_join_a_live_game_they_created(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        self.assertFalse(user_middleware.can_join_game("9XMQ-FXYJ"), "Error! User joined a live game that they have created!")

    def test_user_cannot_join_an_archived_game_they_created(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        game_creator_middleware = GameCreatorMiddleware(self.david.username)
        game_creator_middleware.stop_game("9XMQ-FXYJ")
        self.assertFalse(user_middleware.can_join_game("9XMQ-FXYJ"), "Error! User joined an archived game that they have created!")

    def test_user_cannot_join_an_unpublished_they_created(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        self.assertFalse(user_middleware.can_join_game("13T2-JFRN"), "Error! User joined an archived game that they have created!")

    def test_user_cannot_join_a_game_with_invalid_code_with_invalid_format(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        self.assertFalse(user_middleware.can_join_game("QWERTYUIOP-1234567"), "Error! User joined a game using a valid code with invalid format!")

    def test_user_cannot_join_a_game_with_invalid_code_with_valid_format(self):
        user_middleware = GamePlayerMiddleware(self.david.username)
        self.assertFalse(user_middleware.can_join_game("ABCD-1234"), "Error! User joined a game using a invalid code with valid format!")





