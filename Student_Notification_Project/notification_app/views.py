from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer, ProfileUserSerializer
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated

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
        
        user = serializer.validated_data['user']        
        token, created = Token.objects.get_or_create(user=user)        
        
        return Response({'token': token.key}, status=status.HTTP_200_OK)

#list all users in database
class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()  # Get all users from the database
    serializer_class = CustomUserSerializer

  
# View to retrieve, update, or delete a specific user by id
class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()  
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'student_id'  
   
#users can view and update their profiles
class ProfileUserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()  # Get all users from the database
    serializer_class = ProfileUserSerializer
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can access this view

    def get_object(self):
        # Return the currently authenticated user’s profile
        return self.request.user  # This ensures users can only access their own profile
   
       


