from django.conf import settings
from django.db import models
from django.utils.text import slugify

from markdownx.models import MarkdownxField

from accounts.models import Profile, MainSkill, OtherSkill

PROJECT_STATUS = (('OPEN', 'Open'), ('CLOSED', 'Closed'))

POSITION_STATUS = (('APPLY', 'Apply'), ('FILLED', 'Filled'))

APPLICANT_STATUS = (('APPROVED', 'Approved'), ('REJECTED', 'Rejected'),
                    ('UNDECIDED', 'Undecided'))


class Project(models.Model):
    """Model for Project"""
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              related_name='projects')
    title = models.CharField(max_length=255, unique=True)
    description = MarkdownxField(max_length=2500, default='')
    project_timeline = models.TextField(default='')
    applicant_requirements = models.TextField(max_length=2500, default='')
    project_status = models.CharField(max_length=255,
                                      choices=PROJECT_STATUS,
                                      blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Position(models.Model):
    """Model for project positions to apply"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, default='')
    description = MarkdownxField(default='')
    main_skill = models.ManyToManyField(MainSkill,
                                        related_name='positions_main')
    other_skill = models.ManyToManyField(OtherSkill,
                                         related_name='positions_other')
    position_status = models.CharField(max_length=255,
                                       choices=POSITION_STATUS,
                                       blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Applicant(models.Model):
    """Model for applicant to apply for position in project"""
    user_profile = models.ForeignKey(Profile,
                                     on_delete=models.CASCADE,
                                     related_name='applicants')
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='project_applicants')
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE,
                                 related_name='position_applicants')
    applicant_status = models.CharField(max_length=255,
                                        choices=APPLICANT_STATUS,
                                        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #unique_together = ['user', 'position']
        ordering = ['-created_at']
