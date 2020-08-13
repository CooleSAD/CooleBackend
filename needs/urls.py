# /properties (get bezani all amval), if taeid nashode...
# /properties/<int: pk> (post bezani, if reservable, success and reserve!)
# /properties/me (foreign key)

# mind authentication, Permission Class~~~


from django.urls import path, include

from .views import NeedsListView, NeedView, UserNeedsListView

urlpatterns = [
    path("needs/", NeedsListView.as_view(), name="needs"),
    path("needs/<int:pk>", NeedView.as_view(), name="need"),
    path("needs/me", UserNeedsListView.as_view(), name="user_needs")
]

