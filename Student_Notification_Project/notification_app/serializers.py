from .models import CustomUser, Bus, Notification, Driver, Smartcard, BusAttendanceLog
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate, get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['student_id', 'phone_number', 'email', 'password', 'student_pickup_latitude', 'student_pickup_longitude', 
                  'student_dropoff_latitude', 'student_dropoff_longitude']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = CustomUser(
            student_id=validated_data['student_id'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            parent_name=validated_data['parent_name'],
            student_pickup_latitude=validated_data.get('student_pickup_latitude'),
            student_pickup_longitude=validated_data.get('student_pickup_longitude'),
            student_dropoff_latitude=validated_data.get('student_dropoff_latitude'),
            student_dropoff_longitude=validated_data.get('student_dropoff_longitude'),
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, data):        
        if (data['student_pickup_latitude'] > 90 or data['student_pickup_latitude'] < -90) or \
        (data['student_dropoff_latitude'] > 90 or data['student_dropoff_latitude'] < -90):
            raise ValidationError("Latitude must be between -90 and 90")

        if (data['student_pickup_longitude'] > 180 or data['student_pickup_longitude'] < -180) or \
        (data['student_dropoff_longitude'] > 180 or data['student_dropoff_longitude'] < -180):
            raise ValidationError("Longitude must be between -180 and 180")
        if not data['parent_name'] or len(data['parent_name']) < 3:
            raise ValidationError("Parent name must be at least 3 characters long")
    
        return data
#userprofile
class ProfileUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()  # Ensure this is formatted correctly

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'parent_name', 
                  'student_pickup_latitude', 'student_pickup_longitude', 
                  'student_dropoff_latitude', 'student_dropoff_longitude']
        read_only_fields = ['student_id']  # Prevent modification of student_id
        
    def update(self, instance, validated_data):
        # Update user profile (non-sensitive fields)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.parent_name = validated_data.get('parent_name', instance.parent_name)
        
        # Optional fields (locations)
        instance.student_pickup_latitude = validated_data.get('student_pickup_latitude', instance.student_pickup_latitude)
        instance.student_pickup_longitude = validated_data.get('student_pickup_longitude', instance.student_pickup_longitude)
        instance.student_dropoff_latitude = validated_data.get('student_dropoff_latitude', instance.student_dropoff_latitude)
        instance.student_dropoff_longitude = validated_data.get('student_dropoff_longitude', instance.student_dropoff_longitude)

        instance.save()
        return instance

# Bus Serializer
class BusSerializer(serializers.ModelSerializer):
    drivers = serializers.StringRelatedField(many=True)  # Serialize driver names

    class Meta:
        model = Bus
        fields = ['bus_id', 'bus_speed', 'drivers']

# Driver Serializer
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['driver_id', 'driver_name', 'driver_licence_number', 'driver_phone_number']

# Smartcard Serializer
class SmartcardSerializer(serializers.ModelSerializer):
    student_id = CustomUserSerializer(read_only=True)  

    class Meta:
        model = Smartcard
        fields = ['smartcard_id', 'student_id', 'issue_date', 'status', 'validity']

class BusAttendanceLogSerializer(serializers.ModelSerializer):
    smartcard_id = SmartcardSerializer(read_only=True)  
    bus_id = BusSerializer(read_only=True)  

    class Meta:
        model = BusAttendanceLog
        fields = ['scan_log_id', 'smartcard_id', 'bus_id', 'boarding_timestamp', 'alighting_timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    student_id = CustomUserSerializer(read_only=True)  
    bus_id = BusSerializer(read_only=True)  
    class Meta:
        model = Notification
        fields = ['notification_id', 'bus_id', 'notification_time', 'bus_location_latitude', 'bus_location_longitude', 'student_id', 'notification_message']

    def update_notification_message(self, instance):
        instance.update_notification_message()
        return instance