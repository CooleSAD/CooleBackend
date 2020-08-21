from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event
from cooleBackend import notification


@receiver(post_save, sender=Event)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notification_message = "رویداد جدید : " + instance.name
        # notification.send_push_message(token="ExponentPushToken[ggWzVsP7TQN65JoyQ0vUFT]", message=notification_message)