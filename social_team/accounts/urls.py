from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'accounts'

urlpatterns = [
     path('', views.profile_all, name='profile_all'),
     path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
     path('profile/edit/<int:pk>/', views.profile_edit, name='profile_edit'),
]

urlpatterns += staticfiles_urlpatterns()