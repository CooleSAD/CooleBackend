from rest_framework.authtoken.models import Token
from rest_framework.exceptions import status
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from needs.models import Need
from needs.serializers import NeedSerializer
from users.models import CustomUser


class NeedsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        needs = Need.objects.exclude(is_handled=True).order_by('-created_at')
        serializer = NeedSerializer(needs, many=True)
        for i in range(len(serializer.data)):
            user_id = serializer.data[i].pop('user')
            user = CustomUser.objects.get(pk=user_id)
            serializer.data[i]['user'] = user.profile.nickname
        return Response(serializer.data)

    def post(self, request):

        user = Token.objects.get(key=request.auth).user
        try:
            data = {
                'user': user.id,
                'text': request.data['text'],
                'contact': request.data['contact'],
                'is_handled': False
            }
        except KeyError:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = NeedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            new_data = serializer.data
            user_id = serializer.data.pop('user')
            user = CustomUser.objects.get(pk=user_id)
            new_data['user'] = user.profile.nickname
            return Response(new_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NeedView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        user = Token.objects.get(key=request.auth).user
        need = Need.objects.get(pk=pk)
        if need.user.id != user.id:
            return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
        need.delete()
        return Response({
            'success': True
        })
