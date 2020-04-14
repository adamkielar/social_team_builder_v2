from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify

from cropperjs.models import CropperImageField
from markdownx.models import MarkdownxField
from .choices import POSITIONS


class UserManager(BaseUserManager):
    """Create and save new user"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=False, default='')
    avatar = CropperImageField(default='avatars/sample.png',
                               upload_to='avatars/')
    bio = MarkdownxField(default='')
    date_joined = models.DateTimeField(default=timezone.now)
    main_skills = models.ManyToManyField('MainSkill', related_name=mainskill)
    other_skills = models.ManyToManyField('OtherSkill', related_name=otherskill)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class MainSkill(models.Model):
    """Model for user main skills"""
    main_skill = models.CharField(max_length=255,
                                  choices=POSITIONS,
                                  blank=True)

    def __str__(self):
        return self.main_skill


class OtherSkill(models.Model):
    """Model for user own skills"""
    other_skill = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.other_skill


class UserProject(models.Model):
    """Model for user own project"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_projects')
    project_name = models.CharField(max_length=255, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.project_name
