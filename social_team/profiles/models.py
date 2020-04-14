from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from cropperjs.models import CropperImageField
from markdownx.models import MarkdownxField

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


class Profile(models.Model):
    """Custom user model that supports using email instead of username"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=False, default='')
    avatar = CropperImageField(default='avatars/sample.png',
                               upload_to='avatars/')
    bio = MarkdownxField(default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    main_skills = models.ManyToManyField('MainSkill', related_name='mainskill')
    other_skills = models.ManyToManyField('OtherSkill',
                                          related_name='otherskill')

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
