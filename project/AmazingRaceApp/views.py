from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import generic

from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware


class LoginView(generic.FormView):
    template_name = 'login.html'
    form = AuthenticationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'forms': self.form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return HttpResponseRedirect('/')


class HomepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home.html'
    login_url = '/login'

    player = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)

        return render(request, self.template_name, context={
            'recent_game_ranks': self.player.rank_in_most_recent_games(10)
        })


class LeaderboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'Leaderboard.html'
    login_url = '/login'


class ProfilepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profilepage.html'
    login_url = '/login'


class RegisterView(generic.TemplateView):
    template_name = 'register.html'


class GameCreatedListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-list.html'
    login_url = '/login'

    player = None
    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)

        return render(request, self.template_name, context={
            'page_name' : 'Created',
            'recent_game_ranks': self.player.list_played_games()
        })


class GamePlayedListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-list.html'
    login_url = '/login'

    player = None
    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)

        return render(request, self.template_name, context={
            'page_name': 'Played',
            'games': self.player.list_played_games()
        })