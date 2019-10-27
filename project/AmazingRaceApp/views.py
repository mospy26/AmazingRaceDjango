from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import json
from django.http import HttpResponseRedirect, HttpResponse
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


def handler(request, status_code):
    response = render_to_response(str(status_code) + '.html', {'user': request.user})
    response.status_code = int(status_code)
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

        return render(request, self.template_name, context={
            'games_played': self.player.get_games_played(),
            'games_created': self.creator.get_number_created_games(),
            'name': self.player.get_name(),
            'username': self.player.get_username(),
            'profile_picture': None if not self.player.profilePic else self.player.get_profile_picture()
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
            'games': self.player.created_games(),
            'status': self.player.get_status_of_game('LQGY-M42U')
        })


class GamePlayedListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-list.html'
    login_url = '/login'

    player = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)
        games = self.player.list_played_games()
        return render(request, self.template_name, context={
            'page_name': 'Played',
            'games': games,
            'status': self.player.get_status_of_game('LQGY-M42U')
        })


class GamePlayingListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'play-games.html'
    login_url = '/login'
    player = None

    def get(self, request, *args, **kwargs):
        self.game = _GameMiddleware('LQGY-M42U')
        self.player = GamePlayerMiddleware(request.user.username)
        
        lat_long = []
        visited = self.player.locations_visited('LQGY-M42U')
        for location in visited:
            if location[1] != "???":
                temp = []
                latitude, longitude = self.maps.get_coordinate(location[1])
                temp.append(float(latitude))
                temp.append(float(longitude))
                temp.append(location[1])
                lat_long.append(temp)
            
        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name(),
            'visited': self.player.locations_visited('LQGY-M42U'),
            'lat_long': lat_long
        })


class GameCreationListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-create.html'
    login_url = '/login'
    form = GameRenameForm

    def get(self, request, code, *args, **kwargs):
        # temp game
        self.game_creator = GameCreatorMiddleware(request.user.username)
        game = self.game_creator.get_game(code)

        if not game:
            return handler(request, 403)

        if not self.game_creator.is_authorized_to_access_game(code):
            return handler(request, 403)

        self.maps = MapsMiddleware()

        return render(request, self.template_name, context={
            'locations_code': self.game_creator.get_ordered_locations_of_game(code),
            'game_details': self.game_creator.get_code_and_name(code),
            'code': code,
            'lat_long': self.maps.get_list_of_long_lat(code)
        })

    def post(self, request, *args, **kwargs):

        self.game_creator = GameCreatorMiddleware(request.user.username)

        if not self.game_creator.is_authorized_to_access_game(kwargs['code']) or \
                not self.game_creator.is_live_game(kwargs['code']):
            return handler(request, 403)

        if 'title' in request.POST.keys() and 'code' in kwargs.keys():
            return self._update_title_post_request(request, **kwargs)
        elif 'location_order' in request.POST.keys():
            return self._update_location_order_post_request(request, **kwargs)

    def _update_title_post_request(self, request, *args, **kwargs):
        self.maps = MapsMiddleware()
        self.game_creator = GameCreatorMiddleware(request.user.username)
        self.game = _GameMiddleware(kwargs['code'])
        self.game.change_name(request.POST['title'])
        return render(request, self.template_name, context={
            'locations_code': self.game_creator.get_ordered_locations_of_game(kwargs['code']),
            'game_details': self.game_creator.get_code_and_name(kwargs['code']),
            'code': kwargs['code'],
            'lat_long': self.maps.get_list_of_long_lat(kwargs['code'])
        })

    def _update_location_order_post_request(self, request, *args, **kwargs):
        self.maps = MapsMiddleware()
        self.game_creator = GameCreatorMiddleware(request.user.username)
        codes_order_list = request.POST['location_order'].split(',')
        self.game_creator.update_location_order(codes_order_list, kwargs['code'])
        return render(request, self.template_name, context={
            'locations_code': self.game_creator.get_ordered_locations_of_game(kwargs['code']),
            'game_details': self.game_creator.get_code_and_name(kwargs['code']),
            'code': kwargs['code'],
            'lat_long': self.maps.get_list_of_long_lat(kwargs['code'])
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
        self.maps = MapsMiddleware()
        
        location_name = getattr(next(self.locations.get_location_at_x('LQGY-M42U', 1))[1], 'name')
        
        latitude, longitude = self.maps.get_coordinate(location_name)
        latitude = float(latitude)
        longitude = float(longitude)
        
        return render(request, self.template_name, context={
            'locations_code': self.locations.get_location_at_x('LQGY-M42U', 1),
            'game_details': self.game.get_code_and_name(),
            'game_player_name': self.player.get_name(),
            'game_player_username': self.player.get_username(),
            'lat_long': [latitude, longitude]
        })


class LocationAdd(LoginRequiredMixin, generic.TemplateView):
    template_name = 'addlocation.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.game = _GameMiddleware('LQGY-M42U')
        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name(),
            'lat_long': [-33.865143, 151.209900],
            'location_name': ""
        })
    
    def post(self, request, *args, **kwargs):
        self.game = _GameMiddleware('LQGY-M42U')
        self.maps = MapsMiddleware()
        
        location = request.POST['locationSearch'].title()
        
        try:
            latitude, longitude = self.maps.get_coordinate(request.POST['locationSearch'])
            latitude = float(latitude)
            longitude = float(longitude)
        except:
            latitude = -33.865143
            longitude = 151.209900
            location = location + " * Not Found - Please Try Again *"
        
        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name(),
            'lat_long': [latitude, longitude],
            'location_name': location
        })