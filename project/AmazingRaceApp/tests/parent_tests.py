from django.contrib.auth.models import User
from django.test import TestCase


class DatabaseRequiredTests(TestCase):

    fixtures = [
        'fixtures_user_test',
        'fixtures_game_test',
        'fixtures_gamecreator_test',
        'fixtures_gameplayer_test',
        'fixtures_location_test',
        'fixtures_locationuser_test'
    ]