from django.urls import path, include

from .views import NeedsListView, NeedView

urlpatterns = [
    path("needs/", NeedsListView.as_view(), name="needs"),
    path("needs/<int:pk>", NeedView.as_view(), name="need"),
]

