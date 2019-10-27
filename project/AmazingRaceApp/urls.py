from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('user/', views.ProfilepageView.as_view(), name='user'),
    path('login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user/created/', views.GameCreatedListView.as_view(), name='created'),
    path('user/played/', views.GamePlayedListView.as_view(), name='played'),
    path('game/create/', views.GameCreationListView.as_view(), name = 'create_game'),
    path('game/location/', views.LocationListView.as_view(), name = "locations"),
    path('game/create/<slug:code>', views.GameCreationListView.as_view(), name = 'create_game'),
    path('game/addlocation/', views.LocationAdd.as_view(), name = "add_locations"),
    path('game/leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('game/play/code', views.GamePlayingListView.as_view(), name = 'play_game')
]