from django import forms

from . import models

POSITIONS = (
    ('ANDROID_DEVELOPER', 'Android Developer'),
    ('DESIGNER', 'Designer'),
    ('IOS_DEVELOPER', 'IOS Developer'),
    ('JAVA_DEVELOPER', 'Java Developer'),
    ('PHP_DEVELOPER', 'PHP Developer'),
    ('PYTHON_DEVELOPER', 'Python Developer'),
    ('RAILS_DEVELOPER', 'Rails Developer'),
    ('WORDPRESS_DEVELOPER', 'Wordpress Developer'),
    ('OTHER', 'Other')
)


class ProfileForm(forms.ModelForm):
    """Form for User full_name, bio and image"""
    class Meta:
        model = models.User
        fields = ('full_name', 'bio', 'avatar')

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
        )



class MainSkillForm(forms.ModelForm):
    """Form for User main skill"""
    main_skills = forms.ModelMultipleChoiceField(
        queryset=models.MainSkill.objects.all()
    )

    class Meta:
        model = models.User
        fields = ('main_skills',)

    def clean_main_skills(self):
        data = self.cleaned_data['main_skills']
        if not data:
            raise forms.ValidationError("Please add at least one item to Skills")
        return data


class OtherSkillFormList(forms.ModelForm):
    other_skills = forms.ModelMultipleChoiceField(
        queryset=models.OtherSkill.objects.all()
    )

    class Meta:
        model = models.User
        fields = ('other_skills',)

    def clean_other_skills(self):
        data = self.cleaned_data['other_skills']
        return data


class OtherSkillForm(forms.ModelForm):
    class Meta:
        model = models.OtherSkill
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter Your New Skill'
            }
            )
        }


class UserProjectForm(forms.ModelForm):
    class Meta:
        model = models.UserProject
        fields = ('project_name', 'url')
        widgets = {
            'project_name': forms.TextInput(attrs={
                'placeholder': 'Enter Project Name'
            }
            ),
            'url': forms.TextInput(attrs={
                'placeholder': 'Enter Project Url'
            }
            )
        }


OtherSkillFormSet = forms.modelformset_factory(
    models.OtherSkill,
    form=OtherSkillForm,
    fields=('name', ),
    max_num=2,
)

UserProjectFormSet = forms.modelformset_factory(
    models.UserProject,
    form=UserProjectForm,
    fields=('project_name', 'url'),
    max_num=2,
)
