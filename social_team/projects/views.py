from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from .models import Project, Position, Applicant
from . import forms

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'projects/project.html', {'project': project})
