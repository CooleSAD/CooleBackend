from django.db import models
from users.models import CustomUser

GENDER_CHOICES = [('F', 'female'), ('M', 'male')]


class Event(models.Model):
    name = models.CharField(max_length=100, blank=True)
    length = models.IntegerField()
    date = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    image = models.ImageField()
    participants = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name
