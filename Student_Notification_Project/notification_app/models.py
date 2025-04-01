from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField #type: ignore
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point


from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    student_id = models.IntegerField(unique=True, primary_key=True)
    email = models.EmailField(max_length=254)
    phone_number = models.PhoneNumberField()
    student_pickup_location = gis_models.PointField()
    student_dropoff_location = gis_models.PointField()
    parent_name = models.CharField(max_length=100)


    USERNAME_FIELD = "student_id"
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.student_id} - {self.email}"


class Bus(models.Model):
    bus_id = models.CharField(primary_key=True, max_length=8)
    bus_speed = models.IntegerField()
    drivers = models.ManyToManyField('Driver', related_name='buses')  # Many-to-many relationship

    def __str__(self):
        return self.bus_id
    
    # Method to calculate distance from a target location (latitude, longitude)
    def distance_from(self, latitude, longitude):
        bus_point = Point(self.location.x, self.location.y)  #(longitude, latitude)
        target_point = Point(longitude, latitude)
        return bus_point.distance(target_point)  #Returns distance in meters by default

class Driver(models.Model):
    driver_id = models.CharField(primary_key=True, max_length=50)
    driver_name = models.CharField(max_length=50)
    driver_licence_number = models.CharField( max_length=50)
    driver_phone_number = models.PhoneNumberField()

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
    bus_location = gis_models.PointField()
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_message = models.TextField()

    def __str__(self):
        return f"Notification for Bus {self.bus_id.bus_id} at {self.notification_time}"


