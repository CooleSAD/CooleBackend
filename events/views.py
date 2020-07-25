from rest_framework.authtoken.models import Token
from rest_framework.exceptions import status
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event
from events.serializers import EventSerializer


class EventsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        events = Event.objects.all().order_by('-date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class UserEventListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth).user
        user_events = user.event_set.all().order_by('-date')
        serializer = EventSerializer(user_events, many=True)
        return Response(serializer.data)


class EventEnrollView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        return Response({
            "has_enrolled": user.event_set.filter(pk=pk).exists()
        })

    def post(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        event = Event.objects.get(pk=pk)
        if not user.profile.is_completed or user.profile.gender != event.gender:
            return Response({
                'success': False
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        event.participants.add(user)
        return Response({
            'success': True
        })

    def delete(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        event = Event.objects.get(pk=pk)
        if user.event_set.filter(pk=pk).exists():
            event.participants.remove(user)
            return Response({
                'success': True
            })
        return Response({
            'success': False
        })
