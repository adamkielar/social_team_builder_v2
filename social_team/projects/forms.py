from django import forms

from .models import Project, Position, Applicant
from accounts.models import MainSkill, OtherSkill


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'project_timeline',
            'applicant_requirements',
            'project_status',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Project Title'
                }
            )
        }

class PositionForm(forms.ModelForm):
    main_skills = forms.ModelMultipleChoiceField(
        queryset=MainSkill.objects.all()
    )
    other_skills = forms.ModelMultipleChoiceField(
        queryset=OtherSkill.objects.all()
    )
    class Meta:
        model = Position
        fields = (
            'title',
            'description',
            'main_skills',
            'other_skills',
            'position_status',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Position Title'
                }
            ),
        }

PositionFormSet = forms.modelformset_factory(Position, form=PositionForm)