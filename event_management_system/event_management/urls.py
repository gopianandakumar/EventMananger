from django.urls import path
from .views import EventListCreateView, EventAttendeeListView, EventRegisterView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:event_id>/attendees/', EventAttendeeListView.as_view(), name='event-attendees'),
    path('events/<int:event_id>/register/', EventRegisterView.as_view(), name='event-register'),
]