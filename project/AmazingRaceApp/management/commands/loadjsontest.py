from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Loads all data from the fixtures'
    FIXTURES = [
        'fixtures_user_test',
        'fixtures_game_test',
        'fixtures_gamecreator_test',
        'fixtures_gameplayer_test',
        'fixtures_location_test',
        'fixtures_locationuser_test'
    ]

    def handle(self, *args, **options):
        for fixture in self.FIXTURES:
            call_command('loaddata', fixture)
