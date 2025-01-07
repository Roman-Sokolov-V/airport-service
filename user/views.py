from django.contrib.auth import get_user_model
from django.shortcuts import render

from user.serializers import UserSerializer
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    """Endpoint for creating a new user."""
    serializer_class = UserSerializer


class RetrieveUserView(generics.RetrieveAPIView):
    """Endpoint for retrieving a user."""
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
