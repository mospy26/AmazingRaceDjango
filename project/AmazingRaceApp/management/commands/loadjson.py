from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Loads all data from the fixtures'
    FIXTURES = [
        'fixtures_user',
        'fixtures_game',
        'fixtures_gamecreator',
        'fixtures_gameplayer',
        'fixtures_location',
        'fixtures_locationuser'
    ]

    def handle(self, *args, **options):
        for fixture in self.FIXTURES:
            call_command('loaddata', fixture)
