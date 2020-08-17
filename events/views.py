from rest_framework.authtoken.models import Token
from rest_framework.exceptions import status
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event, Cost
from django.db.models import Sum
from events.serializers import EventSerializer, CostSerializer


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


class EventCostsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        event = Event.objects.get(pk=pk)
        if not event.participants.filter(email=user.email).exists():
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        total_cost = Cost.objects.filter(event=event.id).aggregate(Sum('amount'))['amount__sum']
        each_person_share = total_cost / event.participants.count()
        total_user_cost = Cost.objects.filter(event=event.id, user=user.id).aggregate(Sum('amount'))['amount__sum']
        return Response({'debt': each_person_share - total_user_cost}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        event = Event.objects.get(pk=pk)
        if not event.participants.filter(email=user.email).exists():
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        data = {
            'user': user.id,
            'event': event.id,
            'description': request.data['description'],
            'cost': request.data['cost']
        }
        serializer = CostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class EventCostView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        cost = Cost.objects.get(pk=pk)
        if cost.user.id != user.id:
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        cost.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class UserEventCosts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        event = Event.objects.get(pk=pk)
        if not event.participants.filter(email=user.email).exists():
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CostSerializer(Cost.objects.filter(event=event.id, user=user.id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

