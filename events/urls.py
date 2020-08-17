from django.urls import path

from .views import EventsListView, UserEventListView, EventEnrollView, EventCostsView, UserEventCosts, EventCostView

urlpatterns = [
    path("events/", EventsListView.as_view(), name="events"),
    path("events/me/", UserEventListView.as_view(), name="user_events"),
    path("events/<int:pk>/costs/me/", UserEventCosts.as_view(), name="user_event_costs"),
    path("events/<int:pk>/costs/", EventCostsView.as_view(), name="event_costs"),
    path("events/costs/<int:pk>/", EventCostView.as_view(), name="event_cost"),
    path("events/<int:pk>/", EventEnrollView.as_view(), name="event_enroll"),
]