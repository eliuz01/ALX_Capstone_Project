from django.db import models

# Create your models here.
class Bus(models.Model):
    bus_id = models.CharField(primary_key=True, max_length=8)
    bus_speed = models.IntegerField()

class Driver(models.Model):
    driver_id = models.CharField(primary_key=True, max_length=50)
    driver_name = models.CharField(max_length=50)
    driver_licence_number = models.CharField( max_length=50)
    driver_phone_number = models.IntegerField()

class BusDriverAssignment(models.Model):
    assignment_id = models.CharField(primary_key=True, max_length=50)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    assignment_start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    assignment_end_time = models.DateTimeField(auto_now=False, auto_now_add=False)


class Smartcard(models.Model):
    smartcard_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=False)
    status = models.TextField()
    validity = models.DateField(auto_now_add=False)

class BusAttendanceLog(models.Model):
    scan_log_id = models.IntegerField(primary_key=True, null=False)
    smartcard_id = models.ForeignKey(Smartcard, on_delete=models.CASCADE)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    boarding_timestamp = models.DateTimeField(auto_now_add=True)
    alighting_timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    notification_id = models.IntegerField(primary_key=True)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    notification_time = models.TimeField(auto_now=True)
    bus_location = models.IntegerField()
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)

