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
        logout(request)
        
        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
        response['X-CSRFToken'] = get_token(request)
        
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
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        # Get the group instance
        group = self.get_object()
        
        # Assuming userId is sent in the request data
        user_id = request.data.get('userId')

        # Assuming you have a ManyToMany relationship between Group and User
        try:
            user = User.objects.get(id=user_id)
            group.users.add(user)
            # You may want to customize the response data as needed
            return Response({'message': f'User {user_id} joined group {pk}'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
