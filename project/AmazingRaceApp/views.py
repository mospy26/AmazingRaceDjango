from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import generic
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware
from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware
from AmazingRaceApp.forms import RegisterForm
from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware


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

    player = None
    creator = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)
        self.creator = GameCreatorMiddleware(request.user.username)

        return render(request, self.template_name, context={
            'games_played': self.player.get_games_played(),
            'games_created': self.creator.get_number_created_games()
        })


class RegisterView(generic.TemplateView):
    template_name = 'register.html'
    form = RegisterForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {
            'form': self.form
        })

    def post(self, request, *args, **kwargs):

        form = self.form(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')

        print(form['first_name'].errors)
        return render(request, self.template_name, {
            'form': form
        })


class GameCreatedListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-list.html'
    login_url = '/login'

    player = None

    def get(self, request, *args, **kwargs):
        self.player = GameCreatorMiddleware(request.user.username)

        return render(request, self.template_name, context={
            'page_name' : 'Created',
            'games': self.player.created_games()
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

class GameCreationListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-create.html'
    login_url = '/login'

    locations = None

    def get(self, request, *args, **kwargs):
        self.locations = MapsMiddleware()

        return render(request, self.template_name, context={
            'locations_code': self.locations.get_all_name_code()
        })