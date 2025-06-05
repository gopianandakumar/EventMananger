# Create your models here.
# event_management/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytz

class Event(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")
        if self.max_capacity < 0:
            raise ValidationError("Max capacity cannot be negative")

    def get_attendees_count(self):
        return self.attendees.count()

    def __str__(self):
        return self.name


class Attendee(models.Model):
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'email']

    def __str__(self):
        return f"{self.name} ({self.email})"