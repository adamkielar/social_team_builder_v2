from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'