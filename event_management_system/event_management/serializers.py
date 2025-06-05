from rest_framework import serializers
from .models import Event, Attendee
from django.utils import timezone
import pytz

class EventSerializer(serializers.ModelSerializer):
    attendees_count = serializers.IntegerField(source='get_attendees_count', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'location', 'start_time', 'end_time', 'max_capacity', 'timezone', 'attendees_count']
    
    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time")
        if data['max_capacity'] < 0:
            raise serializers.ValidationError("Max capacity cannot be negative")
        
        # Convert times to target timezone
        target_tz = pytz.timezone(data.get('timezone', 'Asia/Kolkata'))
        data['start_time'] = data['start_time'].astimezone(target_tz)
        data['end_time'] = data['end_time'].astimezone(target_tz)
        return data

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'name', 'email', 'registered_at']


