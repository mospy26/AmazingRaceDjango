from django.shortcuts import render

# Create your views here.
from django.views import generic

from AmazingRaceApp.api.GamePlayerMiddleware import GamePlayerMiddleware


class Test(generic.TemplateView):

    template_name = 'profilepage.html'

    def get(self, request):

        g = GamePlayerMiddleware(username='echa')
        return render(self.request, self.template_name, context={
            'name': g.user.first_name
        })