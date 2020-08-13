from django.db import models
from django.conf import settings

class Need(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    text = models.CharField(max_length=500, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField()

    def __str__(self):
        return self.text
