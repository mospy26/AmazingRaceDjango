import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand

from django.conf import settings


class Command(BaseCommand):
    help = 'Loads all data from the fixtures'
    FIXTURES = {
        'auth.User': 'fixtures_user',
        'AmazingRaceApp.Game': 'fixtures_game',
        'AmazingRaceApp.GameCreator': 'fixtures_gamecreator',
        'AmazingRaceApp.GamePlayer': 'fixtures_gameplayer',
        'AmazingRaceApp.Location': 'fixtures_location',
        'AmazingRaceApp.LocationUser': 'fixtures_locationuser',
    }

    def handle(self, *args, **options):
        for fixture in self.FIXTURES.items():
            sys.stdout = open(settings.BASE_DIR + '/AmazingRaceApp/fixtures/' + fixture[1] + '.json', "w")
            call_command('dumpdata', fixture[0], indent=4, format='json')
