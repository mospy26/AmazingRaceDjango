from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from AmazingRaceApp.models import Game, Location


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name",)

    """
        Adds first name and last name too to the Register form
    """
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class GameTitleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GameTitleForm, self).__init__(*args, **kwargs)
        self.fields['code'].required = False

    class Meta:
        model = Game

        fields = [
            'title',
            'code'
        ]


class GameRenameForm(forms.ModelForm):
    class Meta:
        model = Game

        fields = [
            'title',
            'code'
        ]


class ChangeClueForm(forms.ModelForm):
    class Meta:
        model = Location

        fields = [
            'code',
            'clues'
        ]
