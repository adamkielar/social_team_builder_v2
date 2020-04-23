from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.projects_all, name='projects_all'),
    path('search/', views.projects_search, name='projects_search'),
    path('project/<slug:slug>', views.project_detail, name='project_detail'),
    path('project/edit/<slug:slug>', views.project_edit, name='project_edit'),
    path('project/new/', views.project_new, name='project_new'),
]
