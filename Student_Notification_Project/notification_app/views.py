from django.shortcuts import render
from .models import CustomUser, Bus
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer, ProfileUserSerializer, BusSerializer
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']        
        token, created = Token.objects.get_or_create(user=user)        
        
        return Response({'token': token.key}, status=status.HTTP_200_OK)

#list all users in database
class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()  
    serializer_class = CustomUserSerializer
    permission_classes  = [IsAdminUser]

  
# View to retrieve, update, or delete a specific user by id
class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()  
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'student_id'  
   
#users can view and update their profiles
class ProfileUserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()  
    serializer_class = ProfileUserSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return self.request.user 


# View to list all buses or create a new bus
class BusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bus.objects.all() 
    serializer_class = BusSerializer 
    permission_class = [IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# View to retrieve, update, or delete a bus by ID
class BusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()  
    serializer_class = BusSerializer  
    permission_class = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

   
       


