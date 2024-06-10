from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User, Group

# class UserSerializer(serializers.ModelSerializer):
#     interests = serializers.ListField(child=serializers.CharField(), allow_empty=True)

#     def to_internal_value(self, data):
#         if isinstance(data.get('interests'), str):
#             data['interests'] = [interest.strip() for interest in data['interests'].split(',')]
#         return super().to_internal_value(data)

#     class Meta:
#         model = User
#         fields = ['id', 'name','password', 'interests']

class UserSerializer(serializers.ModelSerializer):
    interests = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def to_internal_value(self, data):
        if isinstance(data.get('interests'), str):
            data['interests'] = [interest.strip() for interest in data['interests'].split(',')]
        return super().to_internal_value(data)

    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'interests']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
