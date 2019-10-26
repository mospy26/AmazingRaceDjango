import string
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware
from AmazingRaceApp.models import Game


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name",)

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
