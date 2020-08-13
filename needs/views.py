from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import status
from rest_framework.authtoken.models import Token

from needs.models import Need
from needs.serializers import NeedSerializer


class NeedsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        needs = Need.objects.exclude(state='C')
        serializer = NeedSerializer(needs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NeedView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        need = Need.objects.get(pk=pk)
        need.is_handled = not need.is_handled
        need.save()
        return Response({
            'success': True
        })


class UserNeedsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Token.objects.get(key=request.auth).user
        user_properties = user.need_set.all()
        serializer = NeedSerializer(user_properties, many=True)
        return Response(serializer.data)
