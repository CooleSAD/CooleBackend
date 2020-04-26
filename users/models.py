from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    city = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=20)
    has_car = models.BooleanField()
    # photo = models.ImageField(upload_to='uploads', blank=True)

    # events_num
    # user current label -> related to permission handling

    def __str__(self):
        return self.user.username

