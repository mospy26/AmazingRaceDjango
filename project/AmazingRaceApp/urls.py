from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.HomepageView.as_view(), name='homapage'),
    path('game/leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('user/', views.ProfilepageView.as_view(), name='user'),
    path('login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='login.html'), name='logout'),
]
