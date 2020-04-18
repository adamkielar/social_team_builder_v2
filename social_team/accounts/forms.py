from django import forms

from accounts import models


class ProfileForm(forms.ModelForm):
    class Meta:
        fields = ('full_name', 'bio', 'avatar')
        model = models.Profile

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
