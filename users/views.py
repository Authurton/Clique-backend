from django.contrib.auth import authenticate
from django.contrib import messages, auth
from rest_framework import viewsets, status
from .models import User, Group
from .serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import firebase_admin
from firebase_admin import firestore
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import logout

db = firestore.client()

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_data = request.data
        db.collection('users').add(user_data)
        return response
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            serializer = UserSerializer(user)
               # Set the session cookie in the response headers
            session_cookie = request.session.session_key
            response = Response(serializer.data)
            response.set_cookie(
                settings.SESSION_COOKIE_NAME,
                session_cookie,
                max_age=settings.SESSION_COOKIE_AGE,
                httponly=True,
                samesite='Lax'  # or 'Strict', depending on your requirements
            )

            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, methods=['get'])
    def current_user(self, request):
        user = request.user
        print(user, 'logged in user')
        if user.is_authenticated:
            groups = user.group_set.values('id', 'group_name')
            user_data = {
                'id': user.id,
                'name': user.name,
                'groups': list(groups)
            }
            return Response(user_data)
        else:
            return Response({'error': 'User not authenticated'}, status=401)
        
    @action(detail=False, methods=['post'])
    def logout(self, request):
        # Log out the current user
        logout(request)
        # Clear the session cookie
        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
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
