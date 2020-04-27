from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
     path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),
     path('profile/edit/<int:pk>/', views.ProfileUpdate.as_view(), name='profile_edit'),
]
