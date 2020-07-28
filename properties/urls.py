# /properties (get bezani all amval), if taeid nashode...
# /properties/<int: pk> (post bezani, if reservable, success and reserve!)
# /properties/me (foreign key)

# mind authentication, Permission Class~~~


from django.urls import path, include

from .views import PropertiesListView, UserPropertiesListView, UserPropertyReserveView

urlpatterns = [
    path("properties/", PropertiesListView.as_view(), name="properties"),
    path("properties/me/", UserPropertiesListView.as_view(), name="user_properties"),
    path("properties/<int:pk>/", UserPropertyReserveView.as_view(), name="property_reserve")
]

