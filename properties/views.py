from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import status
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from properties.models import Property
from properties.serializers import PropertySerializer


class PropertiesListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        properties = Property.objects.exclude(state='C')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)


class UserPropertiesListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth).user
        user_properties = user.property_set.all()
        serializer = PropertySerializer(user_properties, many=True)
        return Response(serializer.data)


class UserPropertyReserveView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        property = Property.objects.get(pk=pk)
        if property.state != 'F':
            return Response({
                'success': False
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        property.state = 'R'
        property.borrower = user
        property.save()
        return Response({
            'success': True
        })

