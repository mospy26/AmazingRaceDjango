from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserView)
router.register(r'games', views.GameView)
router.register(r'locations', views.LocationView)
router.register(r'games-played', views.GamesPlayedView, base_name='games-played')
router.register(r'visited-locations', views.VisitedLocationsView, base_name='visited-locations')

urlpatterns = [
        path('', include(router.urls))
        ]