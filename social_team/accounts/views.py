from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError, transaction
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from .forms import ProfileForm, AvatarForm, UserProjectForm, MainSkillForm
from .models import User, MainSkill


@login_required
def profile_all(request):
    return render(request, 'accounts/index.html')


@login_required
def profile_detail(request, pk):
    mainskills = MainSkill.objects.all().filter(id=pk)
    profile = User.objects.get(pk=pk)
    return render(request, 'accounts/profile.html', {'profile': profile, 'mainskills': mainskills})


@login_required
def profile_edit(request, pk):
    profile_form = ProfileForm(instance=request.user)
    avatar_from = AvatarForm(instance=request.user)
    mainskill_form = MainSkillForm(instance=request.user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user)
        avatar_from = AvatarForm(
            request.POST, request.FILES, instance=request.user
        )
        mainskill_form = MainSkillForm(request.POST, instance=request.user)
        if profile_form.is_valid() and avatar_from.is_valid() and mainskill_form.is_valid():
            profile_form.save()
            avatar_from.save()
            mainskill_form.save()
            messages.success(request, "Profile updated !")
            return HttpResponseRedirect(reverse('accounts:profile_detail', kwargs={'pk': request.user.id}))

    return render(
        request,
        "accounts/profile_form.html",
        {
            "profile_form": profile_form,
            "avatar_form": avatar_from,
            "mainskill_form": mainskill_form,
        },
    )