from rest_framework import viewsets
from .models import User, Group
from .serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import firebase_admin
from firebase_admin import firestore

db = firestore.client()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_data = request.data
        db.collection('users').add(user_data)
        return response

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        group = self.get_object()
        users = group.users.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
