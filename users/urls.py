from django.urls import path, include

from .views import UserProfileView

urlpatterns = [
    path('users/me/', UserProfileView.as_view(), name='user_profile')
]