from django.urls import path, include

from .views import EventsListView

urlpatterns = [
    path("events/", EventsListView.as_view(), name="events"),
]