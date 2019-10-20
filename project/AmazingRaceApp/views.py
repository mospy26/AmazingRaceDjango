from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.views import generic

from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware


class Login(generic.TemplateView):
    template_name = 'topbar.html'


class HomepageView(generic.TemplateView):
    template_name = 'home.html'

    player = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware('echa')

        return render(request, self.template_name, context={
            'recent_game_ranks': self.player.rank_in_most_recent_games(10)
        })


class LeaderboardView(generic.TemplateView):
    template_name = 'Leaderboard.html'


class ProfilepageView(generic.TemplateView):
    template_name = 'profilepage.html'
