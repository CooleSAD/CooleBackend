# /properties (get bezani all amval), if taeid nashode...
# /properties/<int: pk> (post bezani, if reservable, success and reserve!)
# /properties/me (foreign key)

# mind authentication, Permission Class~~~


from django.urls import path, include

from .views import NeedsListView, NeedView

urlpatterns = [
    path("needs/", NeedsListView.as_view(), name="needs"),
    # path("needs/me", UserNeedsListView.as_view(), name="user_needs"),
    path("needs/<int:pk>", NeedView.as_view(), name="need"),
]

