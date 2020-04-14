from django.conf import settings
from django.db import models
from django.utils.text import slugify

from markdownx.models import MarkdownxField

PROJECT_STATUS = (('OPEN', 'Open'), ('CLOSED', 'Closed'))

POSITION_STATUS = (('APPLY', 'Apply'), ('FILLED', 'Filled'))

APPLICANT_STATUS = (('APPROVED', 'Approved'), ('REJECTED', 'Rejected'),
                    ('UNDECIDED', 'Undecided'))


class Project(models.Model):
    """Model for Project"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    description = MarkdownxField(default='')
    project_timeline = models.TextField(default='')
    applicant_requirements = models.TextField(default='')
    project_status = models.CharField(max_length=255,
                                      choices=PROJECT_STATUS,
                                      blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Position(models.Model):
    """Model for project positions to apply"""
    pass


class Applicant(models.Model):
    """Model for user who apply for possition in project"""
    pass

