from django.contrib.auth.models import User

from AmazingRaceApp import forms
from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests
from .. import forms


class TestCreateNewUser(DatabaseRequiredTests):

    def test_register_user_form_is_valid(self):
        form = forms.RegisterForm({
            'first_name': "Hello",
            'last_name': "World",
            'username': "helloworld",
            'password1': "mynameishelloworld123",
            'password2': "mynameishelloworld123"
        })

        self.assertTrue(form.is_valid(), "ERROR! Supposedly valid user creation form is invalid?")

    def test_register_user_form_saves_in_database(self):
        form = forms.RegisterForm({
            'first_name': "Hello",
            'last_name': "World",
            'username': "helloworld",
            'password1': "mynameishelloworld123",
            'password2': "mynameishelloworld123"
        })

        user = form.save()

        self.assertTrue(User.objects.get(username="helloworld"), "ERROR! Form save did not "
                                                                 "reflect in the db")

    def test_register_user_form_should_not_work_with_username_duplicates(self):
        form = forms.RegisterForm({
            'first_name': "Hello",
            'last_name': "World",
            'username': "40wam",  # this username already exists in the db
            'password1': "mynameishelloworld123",
            'password2': "mynameishelloworld123"
        })

        self.assertFalse(form.is_valid())

    def test_register_user_form_should_not_work_with_weak_password(self):
        form = forms.RegisterForm({
            'first_name': "Hello",
            'last_name': "World",
            'username': "helloworld",
            'password1': "he",  # weak passwords
            'password2': "he"
        })

        self.assertFalse(form.is_valid())

    def test_register_user_form_should_not_work_with_not_matching_passwords(self):
        form = forms.RegisterForm({
            'first_name': "Hello",
            'last_name': "World",
            'username': "helloworld",
            'password1': "mynameishelloworld123",  # non matching passwords
            'password2': "notmachingpasswords"
        })

        self.assertFalse(form.is_valid())

    def test_register_user_form_should_not_work_with_empty_username(self):
        form = forms.RegisterForm({
            'first_name': "Hello",
            'last_name': "World",
            'username': "",
            'password1': "mynameishelloworld123",  # non matching passwords
            'password2': "notmachingpasswords"
        })

        self.assertFalse(form.is_valid())