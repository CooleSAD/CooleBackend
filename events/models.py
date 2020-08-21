from django.db import models
from users.models import CustomUser

GENDER_CHOICES = [('F', 'female'), ('M', 'male')]


class Event(models.Model):
    name = models.CharField(max_length=100, blank=True)
    length = models.IntegerField()
    date = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    image = models.ImageField(upload_to='media/', blank=True)
    participants = models.ManyToManyField(CustomUser, blank=True)
    description = models.TextField(max_length=200)
    coordination_date = models.DateField()
    difficulty_level = models.CharField(max_length=50)
    coordinator = models.CharField(max_length=50)
    coordinator_phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Cost(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    description = models.CharField(max_length=200, default=None, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return Event.objects.get(pk=self.event.id).name + "-" + self.description


