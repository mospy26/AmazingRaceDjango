from django.shortcuts import render

# Create your views here.
from django.views import generic


class Test(generic.TemplateView):

    template_name = 'profilepage.html'