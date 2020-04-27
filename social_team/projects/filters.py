import django_filters
from django.db.models import Q

from projects.models import Project, Position, POSITION_STATUS


class PositionStatusFilter(django_filters.FilterSet):
    position_status = django_filters.ChoiceFilter(choices=POSITION_STATUS)

    class Meta:
        model = Position
        fields = ['position_status']


class ProjectsFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = ['project_status']


