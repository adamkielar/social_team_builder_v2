from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('profile/<pk>', views.UserProfile.as_view(), name='user_profile'),
]