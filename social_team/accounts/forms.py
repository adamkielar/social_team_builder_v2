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
    class Meta:
        model = models.User
        fields = ['full_name', 'bio']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['avatar']

    class Media:
        css = {"all": ("/assets/css/global.css", )}
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
        )

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


class MainSkillForm(forms.ModelForm):
    main_skills = forms.ModelMultipleChoiceField(
        queryset=models.MainSkill.objects.all()
    )
    class Meta:
        model = models.User
        fields = ('main_skills', )

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
        fields = ['other_skills']

    def clean_other_skills(self):
        data = self.cleaned_data['other_skills']
        return data

class OtherSkillForm(forms.Form):
    name = forms.CharField(
        label='Add new skill',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Your New Skill'
        })
    )

OtherSkillFormSet = forms.formset_factory(OtherSkillForm, extra=1)

UserProjectFormSet = forms.modelformset_factory(
    models.UserProject, 
    form=UserProjectForm,
    extra=1,
    )


