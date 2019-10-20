from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homapage'),
    path('game/leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('user/profile/', views.ProfilepageView.as_view(), name='user'),
]
