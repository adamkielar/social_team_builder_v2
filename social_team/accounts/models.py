from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.text import slugify
from django.urls import reverse

from cropperjs.models import CropperImageField
from markdownx.models import MarkdownxField

class UserManager(BaseUserManager):
    """Create and save new user"""
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create and save a new super user"""
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=False, default='')
    avatar = CropperImageField(dimensions=(240, 240), default='avatars/sample.png', upload_to='avatars/')
    bio = MarkdownxField()
    date_joined = models.DateTimeField(auto_now_add=True)
    main_skills = models.ManyToManyField('MainSkill', related_name='mainskills')
    other_skills = models.ManyToManyField('OtherSkill', related_name='otherskills')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.full_name


class MainSkill(models.Model):
    """Model for user main skills"""
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class OtherSkill(models.Model):
    """Model for user own skills"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return (OtherSkill, self).save(*args, **kwargs)


class UserProject(models.Model):
    """Model for user own project"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_projects')
    project_name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.project_name

