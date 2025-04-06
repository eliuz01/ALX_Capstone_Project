from django.shortcuts import render
from .models import CustomUser, Bus,Smartcard, Driver, BusAttendanceLog, Notification
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer, ProfileUserSerializer, \
BusSerializer, SmartcardSerializer, DriverSerializer, BusAttendanceLogSerializer, NotificationSerializer
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
    permission_class = [IsAuthenticated]
    
    
# View to retrieve, update, or delete a bus by ID
class BusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()  
    serializer_class = BusSerializer  
    permission_class = [IsAdminUser]

# View to retrieve, update, or delete a smartcard by ID  
class SmartcardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Smartcard.objects.all()
    serializer_class = SmartcardSerializer
    permission_classes = [IsAdminUser]

class SmartcardCreateAPIView(generics.CreateApiView):
    queryset = Smartcard.objects.all()
    serializer_class = SmartcardSerializer
    permission_classes = [IsAdminUser]

class DriverCreateAPIView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAdminUser]

class DriverRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAdminUser]

# View to list and create bus attendance logs
class BusAttendanceLogListCreateView(generics.ListCreateAPIView):
    queryset = BusAttendanceLog.objects.all()
    serializer_class = BusAttendanceLogSerializer
    permission_classes = [IsAdminUser] 

# View to retrieve, update, or delete a bus attendance log by ID
class BusAttendanceLogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusAttendanceLog.objects.all()
    serializer_class = BusAttendanceLogSerializer
    permission_classes = [IsAdminUser]  

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]  # Ensure only admin users can access this

    def perform_create(self, serializer):
        """Override perform_create to add any custom behavior, if needed."""
        # You can add custom logic here, like adding additional fields to the Notification instance
        serializer.save()

# View to retrieve, update, or delete a specific notification by ID
class NotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]  # Ensure only admin users can access this
    lookup_field = 'notification_id'  # The field to search by in the URL


    



   
       


