from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm, UserProjectFormSet, MainSkillForm, \
    OtherSkillFormSet, OtherSkillFormList
from .models import User, OtherSkill, UserProject
from projects.models import Project, Position, Applicant
from projects.forms import SearchForm


class ProfileForAll(DetailView):
    """View to display User profile"""
    model = User
    template_name = 'accounts/profile_all.html'

    def get_queryset(self):
        queryset = super(ProfileForAll, self).get_queryset()
        return queryset.filter(id__iexact=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProfileForAll, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['user_projects'] = UserProject.objects.filter(
            user=self.kwargs['pk'])
        context['projects'] = Project.objects.filter(owner=self.kwargs['pk'])
        context['logged_user'] = get_object_or_404(User,
                                                   id=self.request.user.id)
        return context


class ProfileDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """View to display User profile"""
    model = User
    template_name = 'accounts/profile.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if obj == user:
            return True
        else:
            raise Http404(
                "You are not the owner of this profile !"
            )

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['user_projects'] = UserProject.objects.filter(
            user=self.request.user)
        context['projects'] = Project.objects.filter(owner=self.request.user)
        context['applicants'] = Applicant.objects.filter(
            user_profile=self.request.user)
        return context


class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update user profile. Profile is already created -> see models.py
    """
    model = User
    form_class = ProfileForm
    mainskill_form_class = MainSkillForm
    otherskilllist_form_class = OtherSkillFormList
    otherskill_form_class = OtherSkillFormSet
    userproject_form_class = UserProjectFormSet
    search_form_class = SearchForm
    template_name = 'accounts/profile_form.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if obj == user:
            return True
        else:
            raise Http404(
                "You are not the owner of this profile !"
            )

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy('accounts:profile_detail',
                            kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['search_form'] = self.search_form_class()
            context['form'] = self.form_class(self.request.POST,
                                              self.request.FILES,
                                              instance=self.get_object())
            context['mainskill_form'] = self.mainskill_form_class(
                self.request.POST, instance=self.get_object())
            context['otherskill_list_form'] = self.otherskilllist_form_class(
                self.request.POST,
                instance=self.get_object())
            context['otherskill_formset'] = self.otherskill_form_class(
                self.request.POST,
                queryset=OtherSkill.objects.filter(
                    user=self.get_object()), prefix='otherskill')
            context['userproject_formset'] = self.userproject_form_class(
                self.request.POST,
                queryset=UserProject.objects.filter(
                    user=self.get_object()),
                prefix='userproject')
        else:
            context['projects'] = Project.objects.filter(
                owner=self.get_object())
            context['search_form'] = self.search_form_class()
            context['form'] = self.form_class(instance=self.get_object())
            context['mainskill_form'] = self.mainskill_form_class(
                instance=self.get_object())
            context['otherskill_list_form'] = self.otherskilllist_form_class(
                instance=self.get_object())
            context['otherskill_formset'] = self.otherskill_form_class(
                queryset=OtherSkill.objects.filter(user=self.get_object()),
                prefix='otherskill')
            context['userproject_formset'] = self.userproject_form_class(
                queryset=UserProject.objects.filter(user=self.get_object()),
                prefix='userproject')

        return context

    def form_valid(self, form):
        messages.success(self.request, "Profile updated !")
        context = self.get_context_data()
        otherskill_formset = context['otherskill_formset']
        otherskill_list_form = context['otherskill_list_form']
        mainskill_form = context['mainskill_form']
        userproject_formset = context['userproject_formset']
        self.object.save()
        mainskill_form.instance = self.object
        mainskill_form.save()
        otherskill_list_form.instance = self.object
        otherskill_list_form.save()
        if userproject_formset.is_valid() and userproject_formset.has_changed():
            for form in userproject_formset:
                if form.is_valid():
                    project = form.save(commit=False)
                    project.user = self.object
                    project.save()
        if otherskill_formset.is_valid() and otherskill_formset.has_changed():
            for form in otherskill_formset:
                if form.is_valid():
                    otherskill = form.save(commit=False)
                    otherskill.user = self.object
                    otherskill.save()
                    otherskill = OtherSkill.objects.filter(
                        name=otherskill.name, user=self.object)
                    self.object.other_skills.add(*otherskill)
                    self.object.save()

        return super(ProfileUpdate, self).form_valid(form)
