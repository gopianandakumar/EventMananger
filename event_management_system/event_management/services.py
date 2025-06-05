from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Event, Attendee

class EventService:
    @staticmethod
    @transaction.atomic
    def register_attendee(event_id, name, email):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise ValidationError({"event": "Event does not exist"})

        # Check capacity
        if event.get_attendees_count() >= event.max_capacity:
            raise ValidationError({"capacity": "Event is at full capacity"})
        
        # Check for duplicate registration
        if Attendee.objects.filter(event=event, email=email).exists():
            raise ValidationError({"email": "This email is already registered for the event"})
        
        # Create attendee
        attendee = Attendee.objects.create(
            event=event,
            name=name,
            email=email
        )
        return attendee