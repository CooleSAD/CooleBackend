from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
# from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer



