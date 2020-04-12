from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'