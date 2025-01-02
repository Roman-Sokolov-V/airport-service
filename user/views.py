from django.contrib.auth import get_user_model
from django.shortcuts import render

from user.serializers import UserSerializer
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
