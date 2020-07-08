from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


GENDER_CHOICES = [('F', 'female'), ('M', 'male')]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    city = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=20, blank=True)
    has_car = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

