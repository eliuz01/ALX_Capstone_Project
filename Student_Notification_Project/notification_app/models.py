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
    notification_id = models.AutoField(primary_key=True)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    notification_time = models.TimeField(auto_now=True)
    bus_location_latitude = models.FloatField()
    bus_location_longitude = models.FloatField()
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_message = models.TextField(null=True, blank=True, default="Default notification message.")

    def calculate_distance(self, is_pickup=True):
        """Calculates distance between the bus's current location and the student's location."""
        R = 6371  # Earth radius in kilometers
        lat1 = math.radians(self.bus_location_latitude)  # Bus's current latitude
        lon1 = math.radians(self.bus_location_longitude)  # Bus's current longitude

        if is_pickup:
            lat2 = math.radians(self.student_id.student_pickup_latitude)
            lon2 = math.radians(self.student_id.student_pickup_longitude)
        else:
            lat2 = math.radians(self.student_id.student_dropoff_latitude)
            lon2 = math.radians(self.student_id.student_dropoff_longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c  # Distance in kilometers
        return distance

    def calculate_time_to_pickup(self):
        """Calculates the time it will take the bus to reach the pickup location based on speed."""
        distance = self.calculate_distance(is_pickup=True)  # Distance to pickup location
        
        bus_speed = self.bus_id.bus_speed  # Get bus speed from the Bus model
        
        # Time = Distance / Speed, converted to minutes
        time_to_pickup = (distance / bus_speed) * 60  # Time in minutes
        return time_to_pickup

    def calculate_time_to_dropoff(self):
        """Calculates the time it will take the bus to reach the dropoff location based on speed."""
        distance = self.calculate_distance(is_pickup=False)  # Distance to dropoff location
        
        bus_speed = self.bus_id.bus_speed  # Get bus speed from the Bus model
        
        # Time = Distance / Speed, converted to minutes
        time_to_dropoff = (distance / bus_speed) * 60  # Time in minutes
        return time_to_dropoff

    def update_notification_message(self):
        """Updates the notification message with the calculated times."""
        time_to_pickup = self.calculate_time_to_pickup()
        time_to_dropoff = self.calculate_time_to_dropoff()
        
        # Send notification only if within 5 minutes of pickup/dropoff
        if time_to_pickup <= 5:  # within 5 minutes to pickup
            self.notification_message = (
                f"Bus {self.bus_id.bus_id} is approaching your pickup location. "
                f"Distance: {self.calculate_distance(is_pickup=True):.2f} km. "
                f"Time to pickup: {time_to_pickup:.2f} minutes."
            )
        elif time_to_dropoff <= 5:  # within 5 minutes to dropoff
            self.notification_message = (
                f"Bus {self.bus_id.bus_id} is approaching your dropoff location. "
                f"Distance: {self.calculate_distance(is_pickup=False):.2f} km. "
                f"Time to dropoff: {time_to_dropoff:.2f} minutes."
            )
        else:
            # If it's not within 5 minutes, don't send a notification.
            self.notification_message = "Bus is not near your location yet."

        self.save()  # Save the updated message

    