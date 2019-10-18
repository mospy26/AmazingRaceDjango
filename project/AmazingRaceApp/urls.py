from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.Test.as_view(), name='profilepage'),
    path('login/', views.Login.as_view(), name='login')
]
