from django import forms

from .models import User, MainSkill, OtherSkill, UserProject


class ProfileForm(forms.ModelForm):
    """Form for User full_name, bio and image"""

    class Meta:
        model = User
        fields = ('full_name', 'bio', 'avatar')

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
        )


class MainSkillForm(forms.ModelForm):
    """Form for User main skill"""
    main_skills = forms.ModelMultipleChoiceField(
        queryset=MainSkill.objects.all()
    )

    class Meta:
        model = User
        fields = ('main_skills',)

    def clean_main_skills(self):
        data = self.cleaned_data['main_skills']
        if not data:
            raise forms.ValidationError("Please add at least one item to Skills")
        return data


class OtherSkillFormList(forms.ModelForm):
    other_skills = forms.ModelMultipleChoiceField(
        queryset=OtherSkill.objects.all()
    )

    class Meta:
        model = User
        fields = ('other_skills',)

    def clean_other_skills(self):
        data = self.cleaned_data['other_skills']
        return data

    def __init__(self, *args, **kwargs):
        super(OtherSkillFormList, self).__init__(*args, **kwargs)
        self.fields['other_skills'].queryset = self.instance.other_skills


class OtherSkillForm(forms.ModelForm):
    class Meta:
        model = OtherSkill
        fields = ('name', 'id')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter Your New Skill'
            }
            ),
            'id': forms.HiddenInput(),
        }


class UserProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        fields = ('project_name', 'url', 'id')
        widgets = {
            'project_name': forms.TextInput(attrs={
                'placeholder': 'Enter Project Name'
            }
            ),
            'url': forms.TextInput(attrs={
                'placeholder': 'Enter Project Url'
            }
            ),
            'id': forms.HiddenInput(),
        }


OtherSkillFormSet = forms.modelformset_factory(
    OtherSkill,
    form=OtherSkillForm,
    fields=('name', 'id'),
    extra=1,
    max_num=2,
    can_delete=False,
)

UserProjectFormSet = forms.modelformset_factory(
    UserProject,
    form=UserProjectForm,
    fields=('project_name', 'url', 'id'),
    extra=1,
    max_num=2,
    can_delete=False,
)
