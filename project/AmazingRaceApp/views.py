from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.views import generic

from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware


class Test(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profilepage.html'
    login_url = '/login'

    def get(self, request):
        g = GamePlayerMiddleware(username='echa')
        return render(self.request, self.template_name, context={
            'user': g.user
        })


class Login(generic.TemplateView):
    template_name = 'topbar.html'