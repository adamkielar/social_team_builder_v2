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


class MainSkillForm(forms.ModelForm):
    main_skills = forms.ModelMultipleChoiceField(
        queryset=models.MainSkill.objects.all()
    )
    class Meta:
        model = models.User
        fields = ['main_skills']

    def clean_main_skill(self):
        data = self.cleaned_data['main_skill']
        if not data:
            raise forms.ValidationError("Please add at least one item to Skills")
        return data
