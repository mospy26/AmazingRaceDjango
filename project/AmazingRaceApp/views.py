from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware
from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware
from AmazingRaceApp.api.GameMiddleware import _GameMiddleware
from AmazingRaceApp.forms import RegisterForm, GameRenameForm
from AmazingRaceApp.forms import RegisterForm, GameTitleForm
from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware

from django.shortcuts import render_to_response
from django.template import RequestContext

from AmazingRaceApp.models import GameCreator


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


class HomepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home.html'
    login_url = '/login'

    form = GameTitleForm

    player = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)

        return render(request, self.template_name, context={
            'recent_game_ranks': self.player.rank_in_most_recent_games(10)
        })

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)

        if form.is_valid():
            game = form.save()
            game_creator = GameCreator.objects.create(
                game=game,
                creator=request.user
            )
            return redirect('create_game', game.code)

        return render(request, self.template_name, {
            'form': form
        })


class LeaderboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'Leaderboard.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        # temp game
        self.game_creator = GameCreatorMiddleware(request.user.username)
        self.game = _GameMiddleware('LQGY-M42U')

        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name(),
            'leaderboards': self.game_creator.get_leaderboard('LQGY-M42U')
        })


class ProfilepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profilepage.html'
    login_url = '/login'

    player = None
    creator = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)
        self.creator = GameCreatorMiddleware(request.user.username)
        # self.creator = GameCreatorMiddleware("blam")
        # self.player = GamePlayerMiddleware("blam")

        return render(request, self.template_name, context={
            'games_played': self.player.get_games_played(),
            'games_created': self.creator.get_number_created_games(),
            'name': self.player.get_name(),
            'username': self.player.get_username(),
            'profile_picture': self.player.get_profile_picture()
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
            'page_name': 'Created',
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
    form = GameRenameForm

    def get(self, request, code, *args, **kwargs):
        # temp game
        self.game_creator = GameCreatorMiddleware(request.user.username)
        self.game = _GameMiddleware(code)

        return render(request, self.template_name, context={
            'locations_code': self.game_creator.get_ordered_locations_of_game(code),
            'game_details': self.game.get_code_and_name(),
            'code': code
        })

    def post(self, request, *args, **kwargs):
        self.game_creator = GameCreatorMiddleware(request.user.username)
        self.game = _GameMiddleware(kwargs['code'])
        self.game.change_name(request.POST['title'])
        return render(request, self.template_name, context={
            'locations_code': self.game_creator.get_ordered_locations_of_game(self.game.game.code),
            'game_details': self.game.get_code_and_name(),
            'code': kwargs['code']
        })


class LocationListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'locations.html'
    login_url = '/login'

    locations = None
    player = None
    creator = None

    def get(self, request, *args, **kwargs):
        self.locations = GameCreatorMiddleware(request.user.username)
        self.player = GamePlayerMiddleware(request.user.username)
        self.game = _GameMiddleware('LQGY-M42U')

        return render(request, self.template_name, context={
            'locations_code': self.locations.get_location_at_x('LQGY-M42U', 1),
            'game_details': self.game.get_code_and_name(),
            'game_player_name': self.player.get_name(),
            'game_player_username': self.player.get_username()
        })

class LocationAdd(LoginRequiredMixin, generic.TemplateView):
    template_name = 'addlocation.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.game = _GameMiddleware('LQGY-M42U')
        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name()
        })
