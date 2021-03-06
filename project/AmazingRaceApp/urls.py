from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('start/', views.HomepageLoggedOutView.as_view(), name='homepageLoggedOut'),
    path('', views.HomepageView.as_view(), name='homepage'),
    path('user/', views.ProfilepageView.as_view(), name='user'),
    path('login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user/created/', views.GameCreatedListView.as_view(), name='created'),
    path('user/played/', views.GamePlayedListView.as_view(), name='played'),
    path('game/create/<slug:game_code>/<slug:location_code>', views.LocationListView.as_view(), name="locations"),
    path('game/create/<slug:code>', views.GameCreationListView.as_view(), name='create_game'),
    path('game/create/<slug:code>/new/location', views.LocationAdd.as_view(), name="add_locations"),
    path('game/leaderboard/<slug:code>', views.LeaderboardView.as_view(), name='leaderboard'),
    path('game/play/<slug:code>', views.GamePlayingListView.as_view(), name='play_game'),
]
