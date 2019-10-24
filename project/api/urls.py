from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'games', views.GameView)
router.register(r'users', views.UserView)
router.register(r'locations', views.LocationView)

urlpatterns = router.urls