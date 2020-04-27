from django import forms

from .models import Project, Position, Applicant
from accounts.models import MainSkill, OtherSkill


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search Projects...',
            },
        ))


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
            'id',
            'title',
            'description',
            'main_skills',
            'other_skills',
            'timeline',
            'position_status',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Position Title'
            }
            ),
            'timeline': forms.TextInput(attrs={
                'placeholder': 'Contract Length'
            }
            ),
            'id': forms.HiddenInput(),
        }


PositionFormSet = forms.inlineformset_factory(
    Project,
    Position,
    form=PositionForm,
    fields=(
        'id',
        'title',
        'description',
        'main_skills',
        'other_skills',
        'timeline',
        'position_status',
    ),
    extra=1,
    max_num=1,
    can_delete=True
)
