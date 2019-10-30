from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import template

# Create your views here.
from django.views import generic
from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware
from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware
from AmazingRaceApp.api.GameMiddleware import _GameMiddleware
from AmazingRaceApp.forms import RegisterForm, GameRenameForm, ChangeClueForm
from AmazingRaceApp.forms import RegisterForm, GameTitleForm
from AmazingRaceApp.api.MapsMiddleware import MapsMiddleware

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage, Storage

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
    login_url = '/start'

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
        if 'code' in request.POST.keys() and request.POST['code'] != '':
            game = _GameMiddleware(request.POST['code'])
            if not game.game:
                return render(request, self.template_name, context={
                    'recent_game_ranks': player.rank_in_most_recent_games(10),
                    'game_error': "Oops, incorrect code!"
                })
            else:
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
    login_url = '/start'

    def get(self, request, code, *args, **kwargs):
        # temp game
        self.game_creator = GameCreatorMiddleware(request.user.username)
        self.game_player = GamePlayerMiddleware(request.user.username)

        if not self.game_creator.is_authorized_to_access_game(
                code) and not self.game_player.is_authorized_to_access_game(code):
            return handler(request, 404)

        self.game = _GameMiddleware(code)

        return render(request, self.template_name, context={
            'game_details': self.game.get_code_and_name(),
            'leaderboards': self.game_creator.get_leaderboard(code)
        })


class ProfilepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profilepage.html'
    login_url = '/start'

    player = None
    creator = None
    password_form = None

    def get(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)
        self.creator = GameCreatorMiddleware(request.user.username)
        self.password_form = PasswordChangeForm(request.user)

        return render(request, self.template_name, context={
            'games_played': self.player.get_games_played(),
            'games_created': self.creator.get_number_created_games(),
            'name': self.player.get_name(),
            'username': self.player.get_username(),
            'profile_picture': None if not self.player.profilePic else self.player.get_profile_picture(),
            'password_form': self.password_form
        })

    def post(self, request, *args, **kwargs):
        self.player = GamePlayerMiddleware(request.user.username)
        self.creator = GameCreatorMiddleware(request.user.username)

        uploaded_file = None

        # ----------------------- CHECK -----------------------------------------------------
        try:
            uploaded_file = request.FILES['document']

            fs = FileSystemStorage()
            s = Storage()
            path = "profile_picture/" + request.user.username + "-profile-pic.png"
            fs.delete(path)
            fs.save(path, uploaded_file)

            self.player.update_profile_pictures(path)

            return render(request, self.template_name, context={
                'games_played': self.player.get_games_played(),
                'games_created': self.creator.get_number_created_games(),
                'name': self.player.get_name(),
                'username': self.player.get_username(),
                'profile_picture': self.player.get_profile_picture(),
                'password_form': self.password_form
            })
        except:
            form = PasswordChangeForm(request.user, request.POST)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect('/')

            return render(request, self.template_name, context={
                'games_played': self.player.get_games_played(),
                'games_created': self.creator.get_number_created_games(),
                'name': self.player.get_name(),
                'username': self.player.get_username(),
                # 'profile_picture': self.player.get_profile_picture(),
                'password_form': form
            })
        # --------------------------------------------------------------------


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
    login_url = '/start'

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
    login_url = '/start'

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
    login_url = '/start'
    player = None

    def get(self, request, code, *args, **kwargs):
        self.game = _GameMiddleware(code)

        if not self.game:
            return handler(request, 404)

        self.player = GamePlayerMiddleware(request.user.username)

        if not self.player.is_authorized_to_access_game(code):
            return handler(request, 404)

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

    def post(self, request, *args, **kwargs):
        self.game = _GameMiddleware(request.POST['game_code'])

        if not self.game:
            return handler(request, 404)

        self.player = GamePlayerMiddleware(request.user.username)

        if not self.player.is_authorized_to_access_game(request.POST['game_code']):
            return handler(request, 404)

        error = ""

        if len(request.POST['location_code']) == 9:
            result = self.player.visit_location(request.POST['location_code'], request.POST['game_code'])
            if not result:
                error = "Invalid Game Code"
        else:
            error = "Invalid Game Code"

        self.maps = MapsMiddleware()

        lat_long = []
        visited = self.player.locations_visited(request.POST['game_code'])
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
            'visited': self.player.locations_visited(request.POST['game_code']),
            'lat_long': lat_long,
            'error': error
        })


class GameCreationListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'game-create.html'
    login_url = '/start'
    form = GameRenameForm

    def get(self, request, code, *args, **kwargs):
        # temp game
        self.game_creator = GameCreatorMiddleware(request.user.username)
        game = self.game_creator.get_game(code)

        if not game:
            return handler(request, 404)

        if not self.game_creator.is_authorized_to_access_game(code):
            return handler(request, 404)

        if game.game.live:
            self.template_name = 'game-create-live.html'
        elif game.game.archived:
            self.template_name = 'game-create-archived.html'

        self.maps = MapsMiddleware()

        return render(request, self.template_name, context={
            'locations_code': self.game_creator.get_ordered_locations_of_game(code),
            'game_details': self.game_creator.get_code_and_name(code),
            'code': code,
            'lat_long': self.maps.get_list_of_long_lat(code)
        })

    def post(self, request, *args, **kwargs):

        self.game_creator = GameCreatorMiddleware(request.user.username)

        if not self.game_creator.is_authorized_to_access_game(kwargs['code']):
            return handler(request, 404)

        if 'title' in request.POST.keys() and 'code' in kwargs.keys():
            return self._update_title_post_request(request, **kwargs)
        elif 'location_order' in request.POST.keys():
            return self._update_location_order_post_request(request, **kwargs)
        elif 'game_delete' in request.POST.keys():
            return self._delete_game(request, *args, **kwargs)
        elif 'game_start' in request.POST.keys():
            return self._start_game(request, *args, **kwargs)
        elif 'game_stop' in request.POST.keys() and request.POST['game_stop'] != '':
            return self._stop_game(request, *args, **kwargs)

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

    def _delete_game(self, request, *args, **kwargs):
        self.game_creator.delete_game(request.POST['game_delete'])
        return HttpResponseRedirect('/')

    def _start_game(self, request, *args, **kwargs):
        self.game_creator.start_game(request.POST['game_start'])
        return HttpResponseRedirect('/game/create/' + request.POST['game_start'])

    def _stop_game(self, request, *args, **kwargs):
        self.game_creator.stop_game(request.POST['game_stop'])
        return HttpResponseRedirect('/game/create/' + request.POST['game_stop'])


class LocationListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'locations.html'
    login_url = '/start'

    locations = None
    player = None
    creator = None
    form = ChangeClueForm

    def get(self, request, game_code, location_code, *args, **kwargs):
        self.locations = GameCreatorMiddleware(request.user.username)
        self.game = _GameMiddleware(game_code)
        self.maps = MapsMiddleware()

        this_location = self.locations.get_location_by_code(location_code)

        this_location_copy = self.locations.get_location_by_code(location_code)
        for x in this_location:
            location_name = str(x)

        if not self.locations.is_authorized_to_access_game(game_code):
            return handler(request, 404)

        latitude, longitude = self.maps.get_coordinate(location_name)
        latitude = float(latitude)
        longitude = float(longitude)

        return render(request, self.template_name, context={
            'locations_code': this_location,
            'game_details': self.game.get_code_and_name(),
            'game_player_name': self.locations.get_name(),
            'game_player_username': self.locations.get_username(),
            'lat_long': [latitude, longitude],
            'game_code': self.game.game.code,
            'location_code': this_location_copy.first()
        })

    def post(self, request, game_code, location_code, *args, **kwargs):
        self.locations = GameCreatorMiddleware(request.user.username)
        self.game = _GameMiddleware(game_code)
        self.creator = GameCreatorMiddleware(request.user)
        self.maps = MapsMiddleware()

        if not self.creator.is_authorized_to_access_game(request.POST['game_code']):
            return handler(request, 404)

        if 'delete_location_code' in request.POST.keys():
            return self._delete_location(request, game_code, request.POST['delete_location_code'],
                                         self.locations.get_location_by_code(location_code))
        if 'code' in request.POST.keys():
            return self._change_clue(request, request.POST['game_code'], request.POST['code'], *args, **kwargs)

    def _delete_location(self, request, game_code, location_code, *args, **kwargs):
        self.maps = MapsMiddleware()
        self.maps.delete_location(game_code, location_code)
        return HttpResponseRedirect('/game/create/' + game_code)

    def _change_clue(self, request, game_code, location_code, *args, **kwargs):
        self.creator = GameCreatorMiddleware(None)
        self.creator.user = request.user
        form = self.form(instance=self.creator.get_location_of_game(game_code=game_code, location_code=location_code),
                         data=request.POST)

        if form.is_valid():
            print(request.POST['clues'])
            location = form.save(commit=False)
            location.clues = request.POST['clues']
            location.save()
            return HttpResponseRedirect('/game/create/' + game_code + "/" + location_code)

        print(form.errors)
        print(request.POST)
        return HttpResponseRedirect('/error')


class LocationAdd(LoginRequiredMixin, generic.TemplateView):
    template_name = 'addlocation.html'
    login_url = '/start'

    creator = None

    def get(self, request, code, *args, **kwargs):
        self.game = _GameMiddleware(code)
        self.creator = GameCreatorMiddleware(request.user)

        if not self.creator.is_authorized_to_access_game(code):
            return handler(request, 404)

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
            return handler(request, 404)

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
