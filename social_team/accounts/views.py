from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError, transaction
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from .forms import ProfileForm, AvatarForm, UserProjectFormSet, MainSkillForm, OtherSkillFormSet, OtherSkillFormList
from .models import User, MainSkill, OtherSkill, UserProject
from projects.models import Project, Position, Applicant


def profile_all(request):
    positions = Position.objects.all()
    projects = Project.objects.all()
    return render(request, 'accounts/index.html', {
        'positions': positions,
        'projects': projects,
    })


@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(User, pk=pk)
    user_projects = UserProject.objects.all().filter(pk=request.user.id)
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'user_projects': user_projects
    })


@login_required
def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile_form = ProfileForm(instance=request.user)
    avatar_from = AvatarForm(instance=request.user)
    mainskill_form = MainSkillForm(instance=request.user)
    otherskill_list_form = OtherSkillFormList(instance=request.user)
    otherskill_formset = OtherSkillFormSet()
    userproject_formset = UserProjectFormSet()

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user)
        avatar_from = AvatarForm(request.POST,
                                 request.FILES,
                                 instance=request.user)
        mainskill_form = MainSkillForm(request.POST, instance=request.user)
        otherskill_list_form = OtherSkillFormList(request.POST,
                                                  instance=request.user)
        otherskill_formset = OtherSkillFormSet(request.POST)
        userproject_formset = UserProjectFormSet(request.POST)
        if profile_form.is_valid() and avatar_from.is_valid(
        ) and mainskill_form.is_valid() and otherskill_list_form.is_valid(
        ) and otherskill_formset.is_valid() and userproject_formset.is_valid():
            profile_form.save()
            avatar_from.save()
            mainskill_form.save()
            otherskill_list_form.save()

            for form in otherskill_formset:
                if form.cleaned_data.get('name'):
                    OtherSkill(name=form.cleaned_data.get('name')).save()

            for form in userproject_formset:
                if form.cleaned_data.get(
                        'project_name') and form.cleaned_data.get('url'):
                    project = form.save(commit=False)
                    project.user = user
                    project.save()

            messages.success(request, "Profile updated !")
            return HttpResponseRedirect(
                reverse('accounts:profile_detail',
                        kwargs={'pk': request.user.id}))

    return render(
        request,
        "accounts/profile_form.html",
        {
            "profile_form": profile_form,
            "avatar_form": avatar_from,
            "mainskill_form": mainskill_form,
            "otherskill_list_form": otherskill_list_form,
            "otherskill_formset": otherskill_formset,
            "userproject_formset": userproject_formset,
        },
    )