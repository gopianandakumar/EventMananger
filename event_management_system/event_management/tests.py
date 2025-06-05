import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Event, Attendee
from datetime import timedelta
import pytz

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def event():
    return Event.objects.create(
        name="Test Event",
        location="Test Location",
        start_time=timezone.now() + timedelta(days=1),
        end_time=timezone.now() + timedelta(days=1, hours=2),
        max_capacity=10,
        timezone="Asia/Kolkata"
    )

@pytest.mark.django_db
def test_create_event(api_client):
    event_data = {
        "name": "Test Event",
        "location": "Test Location",
        "start_time": (timezone.now() + timedelta(days=1)).isoformat(),
        "end_time": (timezone.now() + timedelta(days=1, hours=2)).isoformat(),
        "max_capacity": 10,
        "timezone": "Asia/Kolkata"
    }
    response = api_client.post('/events/', event_data)
    assert response.status_code == 201
    assert Event.objects.count() == 1

@pytest.mark.django_db
def test_register_attendee(api_client, event):
    attendee_data = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    response = api_client.post(f'/events/{event.id}/register/', attendee_data)
    assert response.status_code == 201
    assert Attendee.objects.count() == 1

@pytest.mark.django_db
def test_prevent_overbooking(api_client, event):
    event.max_capacity = 1
    event.save()
    
    # Register first attendee
    api_client.post(f'/events/{event.id}/register/', {
        "name": "John Doe",
        "email": "john@example.com"
    })
    
    # Try to register second attendee
    response = api_client.post(f'/events/{event.id}/register/', {
        "name": "Jane Doe",
        "email": "jane@example.com"
    })
    assert response.status_code == 400
    assert "full capacity" in response.data['error']

@pytest.mark.django_db
def test_prevent_duplicate_registration(api_client, event):
    attendee_data = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    api_client.post(f'/events/{event.id}/register/', attendee_data)
    response = api_client.post(f'/events/{event.id}/register/', attendee_data)
    assert response.status_code == 400
    assert "already registered" in response.data['error']
