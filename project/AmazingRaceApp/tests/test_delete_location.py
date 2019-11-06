from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware
from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware
from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests


class DeleteLocationTest(DatabaseRequiredTests):

    def setUp(self):
        super(DeleteLocationTest, self).setUp()
        self.maps = MapsMiddleware()

    def test_can_delete_location_of_not_published_game_of_yours(self):
        maps = MapsMiddleware()
        creator_middleware = GameCreatorMiddleware(self.david.username)
        self.assertTrue(creator_middleware.is_authorized_to_access_game("13T2-JFRN"))

        # delete location
        # we know that if this delete_location returned true, the location order also got refactored correctly
        # due to the implementation of this function
        self.assertTrue(maps.delete_location("13T2-JFRN", "24Q9-72EG"), "ERROR! Cannot delete location of an "
                                                                        "unpublished game of yours")

    def test_can_delete_location_of_live_game_of_yours(self):
        creator_middleware = GameCreatorMiddleware(self.david.username)
        self.assertTrue(creator_middleware.is_authorized_to_access_game("9XMQ-FXYJ"))

        # delete location
        # we know that if this delete_location returned true, the location order also got refactored correctly
        # due to the implementation of this function
        self.assertTrue(self.maps.delete_location("9XMQ-FXYJ", "INOC-7WH8"), "ERROR! Cannot delete location of a live "
                                                                             "game of yours")

    def test_can_delete_location_of_archived_game_of_yours(self):
        creator_middleware = GameCreatorMiddleware(self.david.username)
        self.assertTrue(creator_middleware.is_authorized_to_access_game("9XMQ-FXYJ"))

        # archive the game
        creator_middleware.stop_game("9XMQ-FXYJ")

        # delete location
        # we know that if this delete_location returned true, the location order also got refactored correctly
        # due to the implementation of this function
        self.assertTrue(self.maps.delete_location("9XMQ-FXYJ", "INOC-7WH8"), "ERROR! Cannot delete location of an "
                                                                             "archived game of yours")

    def test_cannot_delete_location_of_game_of_another_creator(self):
        creator_middleware = GameCreatorMiddleware(self.david.username)

        # must not be able to access the game
        # the code won't go past this point so we know that he cannot delete the game of another creator
        # regardless of whether it is live or not
        self.assertFalse(creator_middleware.is_authorized_to_access_game("WS30-8FA3"), "ERROR! Can delete location of "
                                                                                       "a game created by another "
                                                                                       "creator")

    def test_cannot_delete_invalid_location_of_game_of_yours(self):
        creator_middleware = GameCreatorMiddleware(self.david.username)

        # must not be able to access the game
        # the code won't go past this point so we know that he cannot delete the game of another creator
        # whether it is live or not
        self.assertFalse(creator_middleware.is_authorized_to_access_game("WS30-8FA3"))

        # delete invalid location
        self.assertFalse(self.maps.delete_location("9XMQ-FXYJ", "INVALID CODE"), "ERROR! Can delete invalid location "
                                                                                 "of a game of yours")

    def test_cannot_delete_invalid_location_of_game_of_yours_two(self):
        creator_middleware = GameCreatorMiddleware(self.david.username)

        # must not be able to access the game
        # the code won't go past this point so we know that he cannot delete the game of another creator
        # whether it is live or not
        self.assertFalse(creator_middleware.is_authorized_to_access_game("WS30-8FA3"))

        # delete location of another game in this game
        self.assertFalse(self.maps.delete_location("9XMQ-FXYJ", "684V-7K25"), "ERROR! Can delete a location of "
                                                                              "another game which is not in your game")
