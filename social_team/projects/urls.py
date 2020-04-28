from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectAll.as_view(), name='projects_all'),
    path('search/', views.SearchView.as_view(), name='projects_search'),
    path('project/<slug:slug>', views.ProjectDetail.as_view(), name='project_detail'),
    path('project/edit/<slug:slug>', views.ProjectEdit.as_view(), name='project_edit'),
    path('project/new/', views.ProjectCreate.as_view(), name='project_new'),
    path('project/delete/<slug:slug>', views.ProjectDelete.as_view(), name='project_delete'),
    path('applications/', views.ApplicantList.as_view(), name='applications'),
    path('applications/apply/<int:pk>', views.ApplicantCreate.as_view(), name='apply')
]
