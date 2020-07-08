from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import status

from .serializers import UserProfileSerializer


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth).user
        user_profile = user.profile
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        user = Token.objects.get(key=request.auth).user
        user_profile = user.profile
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            if not user_profile.is_completed:
                user_profile.is_completed = True
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

