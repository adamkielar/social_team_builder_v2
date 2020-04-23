from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Project, Position, Applicant
from .forms import ProjectForm, PositionFormSet


def projects_search(request):
    positions = Position.objects.all()
    query = request.GET.get('q')

    if query:
        projects = Project.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
        )
    return render(request, 'projects/search.html', {'projects': projects, 'positions': positions, 'query': query})

def projects_all(request):
    positions = Position.objects.all()
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {
        'positions': positions,
        'projects': projects,
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    positions = Position.objects.all()
    return render(request, 'projects/project.html', {
        'project': project,
        'positions': positions
    })


@login_required
def project_edit(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'projects/project_edit.html', {'project': project})


@login_required
def project_new(request):
    user = request.user
    project = None
    project_form = ProjectForm()
    position_formset = PositionFormSet(queryset=Position.objects.none())

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        position_formset = PositionFormSet(request.POST, queryset=Position.objects.filter(project=project))

        if project_form.is_valid() and position_formset.is_valid():
            project = project_form.save(commit=False)
            project.owner = user
            project.project_status = 'OPEN'
            project = project.save()

            for position in position_formset:
                position = position.save(commit=False)
                position.project = project
                position.status = 'APPLY'
                position.save()

            messages.success(request, "Project created !")
            return HttpResponseRedirect(reverse('projects:projects_all'))
    return render(request, 'projects/project_new.html', {
        'project_form': project_form,
        'position_formset': position_formset
    })
