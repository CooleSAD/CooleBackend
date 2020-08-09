from django.db import models

STATE_CHOICES = [('F', 'free'), ('R', 'reserved'), ('C', 'confirmed')]


class Property(models.Model):
    name = models.CharField(max_length=100, blank=True)
    kind = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='media/properties/')
    state = models.CharField(choices=STATE_CHOICES, max_length=1)

    def __str__(self):
        return self.kind + ": " + self.name
