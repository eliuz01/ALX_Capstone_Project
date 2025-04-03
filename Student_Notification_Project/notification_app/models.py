from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
import math
from .managers import CustomUserManager



# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    student_id = models.IntegerField(unique=True, primary_key=True)
    email = models.EmailField(unique=True, max_length=254)
    phone_number = PhoneNumberField(unique=True)
    student_pickup_latitude = models.FloatField(null=True, blank=True)
    student_pickup_longitude = models.FloatField(null=True, blank=True)
    student_dropoff_latitude = models.FloatField(null=True, blank=True)
    student_dropoff_longitude = models.FloatField(null=True, blank=True)
    parent_name = models.CharField(max_length=100)

    #required fields for user management
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.student_id} - {self.email}"  


class Bus(models.Model):
    bus_id = models.CharField(primary_key=True, max_length=8)
    bus_speed = models.IntegerField()
    drivers = models.ManyToManyField('Driver', related_name='buses')  # Many-to-many relationship

    def __str__(self):
        return self.bus_id
    
class Driver(models.Model):
    driver_id = models.CharField(primary_key=True, max_length=50)
    driver_name = models.CharField(max_length=50)
    driver_licence_number = models.CharField( max_length=50)
    driver_phone_number = PhoneNumberField()

    def __str__(self):
        return self.driver_name

class Smartcard(models.Model):
    smartcard_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=False)
    status = models.TextField()
    validity = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"Smartcard {self.smartcard_id} for Student {self.student_id.student_id}"

class BusAttendanceLog(models.Model):
    scan_log_id = models.IntegerField(primary_key=True, null=False)
    smartcard_id = models.ForeignKey(Smartcard, on_delete=models.CASCADE)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    boarding_timestamp = models.DateTimeField(auto_now_add=True)
    alighting_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Log for Smartcard {self.smartcard_id.smartcard_id} on Bus {self.bus_id.bus_id}"

class Notification(models.Model):
    notification_id = models.IntegerField(primary_key=True)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    notification_time = models.TimeField(auto_now=True)
    bus_location_latitude = models.FloatField()
    bus_location_longitude = models.FloatField()
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_message = models.TextField()

    def __str__(self):
        return f"Notification for student{self.student_id.student_id} in {self.bus_id.bus_id} at {self.notification_time}"

    def calculate_distance_to_pickup(self):
        student = self.student_id         
        pickup_lat = student.student_pickup_latitude
        pickup_lon = student.student_pickup_longitude        
        
        bus_lat = self.bus_location_latitude
        bus_lon = self.bus_location_longitude
        
        # Haversine formula to calculate the distance
        return self._calculate_haversine_distance(bus_lat, bus_lon, pickup_lat, pickup_lon)

    def calculate_distance_to_dropoff(self):        
        student = self.student_id  
        dropoff_lat = student.student_dropoff_latitude  
        dropoff_lon = student.student_dropoff_longitude  
        
        bus_lat = self.bus_location_latitude
        bus_lon = self.bus_location_longitude
        
        # Haversine formula to calculate the distance
        return self._calculate_haversine_distance(bus_lat, bus_lon, dropoff_lat, dropoff_lon)

    def _calculate_haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in kilometers
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c  # Distance in kilometers
        return distance
    
    def update_notification_message(self):
        pickup_distance = self.calculate_distance_to_pickup()
        
        dropoff_distance = self.calculate_distance_to_dropoff()
        
        self.notification_message = (
            f"Bus {self.bus_id.bus_id} is approaching. "
            f"Distance to pickup location: {pickup_distance:.2f} km. "
            f"Distance to dropoff location: {dropoff_distance:.2f} km."
        )
        self.save()
