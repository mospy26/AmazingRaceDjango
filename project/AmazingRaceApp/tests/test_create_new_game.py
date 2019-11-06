from django.contrib.auth.models import User

from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests
from AmazingRaceApp.models import Game
from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware

from AmazingRaceApp.forms import GameTitleForm
from .. import forms


class CreateNewGameTest(DatabaseRequiredTests):

    def test_create_game_title_is_valid(self):
        title_of_game = "a"*50 

        form_data = {'title': title_of_game}
        form = GameTitleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_game_title_is_invalid(self):
        title_of_game = "a" * 51

        form_data = {'title': title_of_game}
        form = GameTitleForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_game_title_is_submitted(self):
        form = forms.GameTitleForm({
            'title': "Hello World",
        })

        self.assertTrue(form.is_valid(), "ERROR! Supposedly valid game creation form is invalid?")

    def test_create_game_title_not_submitted(self):
        title = "a" * 51
        form = forms.GameTitleForm({
            'title': title,
        })

        self.assertFalse(form.is_valid(), "ERROR! Supposedly invalid game creation form is valid?")

