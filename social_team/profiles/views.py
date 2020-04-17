from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.views import generic

from profiles import models, forms


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = models.Profile
    template_name = 'profiles/profile.html'

    def get(self, request, *args, **kwargs):
        profiles = get_object_or_404(models.Profile, slug=self.kwargs.get('slug'))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__profile__slug__iexact=self.kwargs.get('slug')
        )


class UserProfileEdit(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.ProfileForm
    model = models.Profile
    template_name = 'profiles/profile_edit.html'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            return super().form_valid(form)

    def get_redirect_url(self, *args, **kwargs):
        return self.get_object().get_absolute_url()