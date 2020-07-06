from django.urls import path, include

from .views import EventsListView, UserEventListView, EventEnrollView

urlpatterns = [
    path("events/", EventsListView.as_view(), name="events"),
    path("events/me/", UserEventListView.as_view(), name="user_events"),
    path("events/<int:pk>/", EventEnrollView.as_view(), name="event_enroll")
]