from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import template

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

class HomepageLoggedOutView(generic.TemplateView):
    template_name = 'homepage2.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={})


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
        player = GamePlayerMiddleware(request.user.username)
        form = self.form(request.POST)

        if 'code' in request.POST.keys() and request.POST['code'] != ['']:
            game = _GameMiddleware(request.POST['code'])
            if not game.game:
                return render(request, self.template_name, context={
                    'recent_game_ranks': player.rank_in_most_recent_games(10),
                    'game_error': "Oops, incorrect code!"
                })
            else:
                print(request.POST['code'])
                if player.can_join_game(request.POST['code']):
                    player.join_game(request.POST['code'])
                    return HttpResponseRedirect("/game/leaderboard/" + request.POST['code'])
                else:
                    return render(request, self.template_name, context={
                        'recent_game_ranks': player.rank_in_most_recent_games(10),
                        'game_error': "Oops, incorrect code!"
                    })

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

    def get(self, request, code, *args, **kwargs):
        # temp game
        self.game_creator = GameCreatorMiddleware(request.user.username)
        self.game_player = GamePlayerMiddleware(request.user.username)

        if not self.game_creator.is_authorized_to_access_game(
                code) and not self.game_player.is_authorized_to_access_game(code):
            return handler(request, '403')

        self.game = _GameMiddleware(code)

        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name(),
            'leaderboards': self.game_creator.get_leaderboard(code)
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

        return render(request, self.template_name, {
            'form': form
        })


class GameCreatedListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-list.html'
    login_url = '/login'

    player = None

    def get(self, request, *args, **kwargs):
        self.player = GameCreatorMiddleware(request.user.username)

        game_status = []
        for x in self.player.created_games():
            game_status.append(self.player.get_status_of_game(x.code))

        return render(request, self.template_name, context={
            'page_name': 'Created',
            'game_and_status': zip(self.player.created_games(), game_status)
        })


class GamePlayedListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-list.html'
    login_url = '/login'

    player = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)
        games = self.player.list_played_games()

        game_status = []
        for x in self.player.list_played_games():
            game_status.append(self.player.get_status_of_game(x[0].code))

        return render(request, self.template_name, context={
            'page_name': 'Played',
            'game_and_status': zip(games, game_status)
        })


class GamePlayingListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'play-games.html'
    login_url = '/login'
    player = None

    def get(self, request, code, *args, **kwargs):
        self.game = _GameMiddleware(code)

        if not self.game:
            return handler(request, '404')

        self.player = GamePlayerMiddleware(request.user.username)

        if not self.player.is_authorized_to_access_game(code):
            return handler(request, '404')

        self.maps = MapsMiddleware()

        lat_long = []
        visited = self.player.locations_visited(code)
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
            'visited': self.player.locations_visited(code),
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
                self.game_creator.is_live_game(kwargs['code']):
            return handler(request, 403)

        if 'title' in request.POST.keys() and 'code' in kwargs.keys():
            return self._update_title_post_request(request, **kwargs)
        elif 'location_order' in request.POST.keys():
            return self._update_location_order_post_request(request, **kwargs)
        elif 'delete' in request.POST.keys():
            return self._delete_game(kwargs['code'])

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

    def _delete_game(self, request, code, *args, **kwargs):
        self.game_creator = GameCreatorMiddleware(request.user.username)
        self.game_creator.delete_game(code)


class LocationListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'locations.html'
    login_url = '/login'

    locations = None
    player = None
    creator = None

    def get(self, request, game_code, location_code, *args, **kwargs):
        self.locations = GameCreatorMiddleware(request.user.username)
        self.game = _GameMiddleware(game_code)
        self.maps = MapsMiddleware()

        this_location = self.locations.get_location_by_code(location_code)

        if not self.locations.is_authorized_to_access_game(game_code):
            return handler(request, '404')

        location_name = getattr(next(self.locations.get_location_at_x(game_code, 1)), 'name')

        latitude, longitude = self.maps.get_coordinate(location_name)
        latitude = float(latitude)
        longitude = float(longitude)

        return render(request, self.template_name, context={
            'locations_code': this_location,
            'game_details': self.game.get_code_and_name(),
            'game_player_name': self.locations.get_name(),
            'game_player_username': self.locations.get_username(),
            'lat_long': [latitude, longitude]
        })

    def post(self, request, code, location_code, *args, **kwargs):
        self.game = _GameMiddleware(code)
        self.creator = GameCreatorMiddleware(request.user)
        self.maps = MapsMiddleware()

        if not self.creator.is_authorized_to_access_game(code):
            return handler(request, '404')

        if 'delete_location' in request.POST.keys():
            self._delete_location(code, self.locations.get_location_by_code(location_code))

    def _delete_location(self, request, game_code, location_code, *args, **kwargs):
        self.maps = MapsMiddleware()
        self.maps.delete_location(game_code, location_code)

class LocationAdd(LoginRequiredMixin, generic.TemplateView):
    template_name = 'addlocation.html'
    login_url = '/login'

    creator = None

    def get(self, request, code, *args, **kwargs):
        self.game = _GameMiddleware(code)
        self.creator = GameCreatorMiddleware(request.user)

        if not self.creator.is_authorized_to_access_game(code):
            return handler(request, '404')

        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name(),
            'lat_long': [-33.865143, 151.209900],
            'location_name': ""
        })

    def post(self, request, code, *args, **kwargs):
        self.game = _GameMiddleware(code)
        self.creator = GameCreatorMiddleware(request.user)
        self.maps = MapsMiddleware()

        if not self.creator.is_authorized_to_access_game(code):
            return handler(request, '404')

        if 'location_order' in request.POST.keys():
            location = request.POST['location_order'].title().strip()
            return self._add_location(request, code, location)

        elif 'locationSearch' in request.POST.keys():
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
                'location_name': location,
                'code': code
            })

    def _add_location(self, request, code, location):
        created = self.maps.create_game_location(code, location)
        return HttpResponseRedirect('/game/create/' + code + "/" + created.code)

    # LQGY-M42U echa creatoed
