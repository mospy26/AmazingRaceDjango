from django.contrib.auth.models import User
from django.test import TestCase

from AmazingRaceApp.models import GameCreator, Game


class DatabaseRequiredTests(TestCase):

    fixtures = [
        'fixtures_user_test',
        'fixtures_game_test',
        'fixtures_gamecreator_test',
        'fixtures_gameplayer_test',
        'fixtures_location_test',
        'fixtures_locationuser_test'
    ]

    def setUp(self):
        self.init_david()

    def init_david(self):
        self.david = User.objects.get(first_name="David")
        self.david_game_creator = GameCreator.objects.filter(creator=self.david).select_related('game')
        self.david_created_games = self.david_game_creator.values('game')
