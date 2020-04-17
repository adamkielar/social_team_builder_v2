from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('profile/<slug:slug>/',
         views.UserProfile.as_view(),
         name='user_profile'),
    path('profile/edit/<slug:slug>/',
         views.UserProfileEdit.as_view(),
         name='user_profile_edit'),
]