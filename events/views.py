from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from events.models import Event
from events.serializers import EventSerializer


class EventsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class UserEventListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth).user
        user_events = user.event_set.all()
        serializer = EventSerializer(user_events, many=True)
        return Response(serializer.data)


class EventEnrollView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        event = Event.objects.get(pk=pk)
        event.participants.add(user)
        return Response({
            'success': True
        })