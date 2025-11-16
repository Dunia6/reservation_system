from rest_framework import serializers
from .models import User, Profile

# Imports


class LoginSerializer(serializers.Serializer):
    """ Serializer for user login. """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    """ Serializer for user profile. """
    class Meta:
        model = Profile
        fields = ['role',]


class UserDetailSerializer(serializers.ModelSerializer):
    """ Serializer for user details. """
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile']
