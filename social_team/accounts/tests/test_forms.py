from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from accounts.models import User
from accounts.forms import ProfileForm, MainSkillForm
