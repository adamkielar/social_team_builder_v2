from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from profiles import models


class HomePageView(TemplateView):
    template_name = 'index.html'