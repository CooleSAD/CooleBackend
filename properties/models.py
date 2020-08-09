from django.db import models
from users.models import CustomUser

STATE_CHOICES = [('F', 'free'), ('R', 'reserved'), ('C', 'confirmed')]


class Property(models.Model):
    name = models.CharField(max_length=100, blank=True)
    kind = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='media/')
    state = models.CharField(choices=STATE_CHOICES, max_length=1)
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return self.kind + ": " + self.name
