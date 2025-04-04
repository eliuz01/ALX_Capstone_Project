from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        # Validate login credentials using the serializer, raise exception if invalid
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # If valid, get the authenticated user object from the serializer's validated data
        user = serializer.validated_data['user']
        
        # Retrieve or create a token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)
        
        # Return the token in the response
        return Response({'token': token.key}, status=status.HTTP_200_OK)
   
       


