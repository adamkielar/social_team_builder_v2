from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic

from profiles import models


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = models.Profile
    template_name = 'profiles/profile.html'
