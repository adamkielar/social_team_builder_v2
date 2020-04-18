from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('profile/<int:pk>/',
         views.UserProfile.as_view(),
         name='user_profile'),
    path('profile/edit/<int:pk>/',
         views.UserProfileEdit.as_view(),
         name='user_profile_edit'),
]