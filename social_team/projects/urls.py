from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('project/<slug:slug>', views.project_detail, name='project_detail'),
]
