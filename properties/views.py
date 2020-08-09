from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import status
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from properties.models import Property
from properties.serializers import EventSerializer


# Create your views here.
# PropertiesListView, UserPropertiesListView, UserPropertyReserveView

class PropertiesListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        properties = Property.objects.exclude(state=2).order_by('-date')
        serializer = EventSerializer(properties, many=True)
        return Response(serializer.data)


class UserPropertiesListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth).user
        user_properties = user.property_set.all().order_by('-date')
        serializer = EventSerializer(user_properties, many=True)
        return Response(serializer.data)


class UserPropertyReserveView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        return Response({
            "has_reserved": user.property_set.filter(pk=pk).exists()
        })

    def post(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        property = Property.objects.get(pk=pk)
        if not user.profile.is_completed or property.state != 0:
            return Response({
                'success': False
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        # TODO: property.participants.add(user)
        return Response({
            'success': True
        })

    def delete(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        property = Property.objects.get(pk=pk)
        if user.property_set.filter(pk=pk).exists():
            # TODO: property.participants.remove(user)
            return Response({
                'success': True
            })
        return Response({
            'success': False
        })

### PROBLEM: LINE 57, 48: how to assign property to a user??!, + event_set??
