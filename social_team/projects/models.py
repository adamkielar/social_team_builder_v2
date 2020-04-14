from django.conf import settings
from django.db import models

PROJECT_STATUS = (
    ('OPEN', 'Open'),
    ('CLOSED', 'Closed')
)

POSITION_STATUS = (
    ('APPLY', 'Apply'),
    ('FILLED', 'Filled')
)

APPLICANT_STATUS = (
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('UNDECIDED', 'Undecided')
)

class Project(models.Model):
    """Model for Project"""
    pass


class Position(models.Model):
    """Model for project positions to apply"""
    pass


class Applicant(models.Model):
    """Model for user who apply for possition in project"""
    pass


