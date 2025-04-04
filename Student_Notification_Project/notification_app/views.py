from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

   
       


