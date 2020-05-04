import django_filters
from django.db.models import Q

from projects.models import Project, Position, Applicant, POSITION_STATUS, APPLICANT_STATUS


class PositionStatusFilter(django_filters.FilterSet):
    position_status = django_filters.ChoiceFilter(choices=POSITION_STATUS)

    class Meta:
        model = Position
        fields = ['position_status']


class ProjectsFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['project_status']


class ApplicantsFilter(django_filters.FilterSet):
    applicant_status = django_filters.ChoiceFilter(choices=APPLICANT_STATUS)

    class Meta:
        model = Applicant
        fields = ['applicant_status']
