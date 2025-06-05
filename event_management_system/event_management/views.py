
from jsonschema import ValidationError
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils import timezone
from .models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer
from .services import EventService
from rest_framework.exceptions import ValidationError as DRFValidationError

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(start_time__gte=timezone.now())
    serializer_class = EventSerializer

class EventAttendeeListView(generics.ListAPIView):
    serializer_class = AttendeeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Attendee.objects.filter(event_id=event_id)

class EventRegisterView(generics.GenericAPIView):
    serializer_class = AttendeeSerializer

    def post(self, request, event_id):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            attendee = EventService.register_attendee(
                event_id=event_id,
                name=serializer.validated_data['name'],
                email=serializer.validated_data['email']
            )
            
            return Response(AttendeeSerializer(attendee).data, status=status.HTTP_201_CREATED)
        
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)