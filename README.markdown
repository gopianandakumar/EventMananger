# Mini Event Management System

This is a Django REST Framework (DRF) application for managing events and attendee registrations. It supports creating events, listing upcoming events, registering attendees, and retrieving attendee lists, with timezone-aware scheduling and validation.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Running the Project](#running-the-project)
4. [API Endpoints](#api-endpoints)
   - [Create an Event](#1-create-an-event)
   - [List Upcoming Events](#2-list-upcoming-events)
   - [Register an Attendee](#3-register-an-attendee)
   - [List Attendees for an Event](#4-list-attendees-for-an-event)
5. [Testing with Postman](#testing-with-postman)
6. [Testing with Swagger](#testing-with-swagger)
7. [Troubleshooting](#troubleshooting)
8. [Project Structure](#project-structure)

## Prerequisites
- **Python**: 3.10 or higher (tested with 3.13.0)
- **PostgreSQL**: 12 or higher
- **Git**: For cloning the repository
- **Virtualenv** (optional, but recommended)
- **Postman** or **Thunder Client** (for API testing)
- **Browser** (for Swagger UI)

Required Python packages (listed in `requirements.txt`):
```
django>=5.2.2
djangorestframework>=3.15.2
drf-yasg>=1.21.7
psycopg2-binary>=2.9.9
pytz>=2023.3
```

## Project Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd event_management_system
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv events
   source events/bin/activate  # Linux/Mac
   events\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL Database**:
   - Install PostgreSQL and create a database named `event_db`:
     ```sql
     CREATE DATABASE event_db;
     ```
   - Update `settings.py` with your PostgreSQL credentials:
     ```python
     # event_management_system/settings.py
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'event_db',
             'USER': 'postgres',  # Your PostgreSQL username
             'PASSWORD': 'your_password',  # Your PostgreSQL password
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Optional)**:
   For accessing the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Project
1. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   - The server runs at `http://localhost:8000`.

2. **Access Endpoints**:
   - **API Root**: `http://localhost:8000/`
   - **Swagger UI**: `http://localhost:8000/swagger/`
   - **Django Admin**: `http://localhost:8000/admin/` (login with superuser credentials)

## API Endpoints
All APIs are accessible at `http://localhost:8000`. Below are the details for each endpoint, including example payloads and responses.

### 1. Create an Event
- **Endpoint**: `POST /events/`
- **Description**: Creates a new event with name, location, start/end times, max capacity, and timezone.
- **Request Body**:
  ```json
  {
      "name": "string",
      "location": "string",
      "start_time": "YYYY-MM-DDTHH:MM:SSZ",
      "end_time": "YYYY-MM-DDTHH:MM:SSZ",
      "max_capacity": integer,
      "timezone": "string"
  }
  ```
- **Example Request**:
  ```json
  {
      "name": "Tech Conference",
      "location": "Convention Center",
      "start_time": "2025-06-10T09:00:00Z",
      "end_time": "2025-06-10T17:00:00Z",
      "max_capacity": 100,
      "timezone": "Asia/Kolkata"
  }
  ```
- **Response** (201 Created):
  ```json
  {
      "id": 1,
      "name": "Tech Conference",
      "location": "Convention Center",
      "start_time": "2025-06-10T14:30:00+05:30",
      "end_time": "2025-06-10T22:30:00+05:30",
      "max_capacity": 100,
      "timezone": "Asia/Kolkata",
      "attendees_count": 0
  }
  ```
- **Error Responses**:
  - 400 Bad Request (e.g., end time before start time):
    ```json
    {"error": "End time must be after start time"}
    ```
  - 400 Bad Request (e.g., negative capacity):
    ```json
    {"error": "Max capacity cannot be negative"}
    ```

### 2. List Upcoming Events
- **Endpoint**: `GET /events/`
- **Description**: Retrieves a list of upcoming events (start_time >= current time).
- **Example Request**: `GET http://localhost:8000/events/`
- **Response** (200 OK):
  ```json
  [
      {
          "id": 1,
          "name": "Tech Conference",
          "location": "Convention Center",
          "start_time": "2025-06-10T14:30:00+05:30",
          "end_time": "2025-06-10T22:30:00+05:30",
          "max_capacity": 100,
          "timezone": "Asia/Kolkata",
          "attendees_count": 0
      }
  ]
  ```
- **Notes**: Returns an empty list `[]` if no upcoming events exist.

### 3. Register an Attendee
- **Endpoint**: `POST /events/{event_id}/register/`
- **Description**: Registers an attendee for a specific event, preventing overbooking or duplicate emails.
- **Request Body**:
  ```json
  {
      "name": "string",
      "email": "string"
  }
  ```
- **Example Request**:
  ```json
  {
      "name": "John Doe",
      "email": "john.doe@example.com"
  }
  ```
- **URL**: `POST http://localhost:8000/events/1/register/`
- **Response** (201 Created):
  ```json
  {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "registered_at": "2025-06-05T19:52:00+05:30"
  }
  ```
- **Error Responses**:
  - 400 Bad Request (e.g., duplicate email):
    ```json
    {"error": "This email is already registered for the event"}
    ```
  - 400 Bad Request (e.g., event full):
    ```json
    {"error": "Event is at full capacity"}
    ```
  - 404 Not Found (invalid event_id):
    ```json
    {"error": "Event not found"}
    ```
  - 400 Bad Request (invalid data):
    ```json
    {"email": ["This field is required"]}
    ```

### 4. List Attendees for an Event
- **Endpoint**: `GET /events/{event_id}/attendees/`
- **Description**: Retrieves a paginated list of attendees for a specific event.
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `page_size`: Items per page (default: 10, max: 100)
- **Example Request**: `GET http://localhost:8000/events/1/attendees/?page=1&page_size=10`
- **Response** (200 OK):
  ```json
  {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
          {
              "id": 1,
              "name": "John Doe",
              "email": "john.doe@example.com",
              "registered_at": "2025-06-05T19:52:00+05:30"
          }
      ]
  }
  ```
- **Error Responses**:
  - 404 Not Found (invalid event_id):
    ```json
    {"error": "Event not found"}
    ```

## Testing with Postman
1. **Setup**:
   - Create a new Postman collection named "Event Management API".
   - Set headers for all POST requests: `Content-Type: application/json`.

2. **Test Cases**:
   - **Create Event**:
     - Method: POST
     - URL: `http://localhost:8000/events/`
     - Body:
       ```json
       {
           "name": "Tech Conference",
           "location": "Convention Center",
           "start_time": "2025-06-10T09:00:00Z",
           "end_time": "2025-06-10T17:00:00Z",
           "max_capacity": 100,
           "timezone": "Asia/Kolkata"
       }
       ```
     - Expected: 201 Created
   - **List Events**:
     - Method: GET
     - URL: `http://localhost:8000/events/`
     - Expected: 200 OK, list of events
   - **Register Attendee**:
     - Method: POST
     - URL: `http://localhost:8000/events/1/register/`
     - Body:
       ```json
       {
           "name": "John Doe",
           "email": "john.doe@example.com"
       }
       ```
     - Expected: 201 Created
     - Test duplicate email:
       - Same body, expect: `{"error": "This email is already registered for the event"}`, 400 Bad Request
   - **List Attendees**:
     - Method: GET
     - URL: `http://localhost:8000/events/1/attendees/?page=1&page_size=10`
     - Expected: 200 OK, paginated attendee list

3. **CSRF Handling**:
   - If CSRF errors occur, include a CSRF token in the `X-CSRFToken` header or disable CSRF for testing (see [Troubleshooting](#troubleshooting)).

## Testing with Swagger
1. **Access Swagger UI**:
   - Open `http://localhost:8000/swagger/` in a browser.
   - Displays all endpoints with schemas.

2. **Test Endpoints**:
   - Expand an endpoint (e.g., `POST /events/`).
   - Click "Try it out".
   - Enter the request body or parameters.
   - Click "Execute" to view the response.
   - Example:
     - For `POST /events/1/register/`:
       - Set `event_id`: 1
       - Body:
         ```json
         {
             "name": "Jane Doe",
             "email": "jane.doe@example.com"
         }
         ```
       - Expect: 201 Created or 400 Bad Request for duplicates.

## Troubleshooting
- **Database Connection Error**:
  - Ensure PostgreSQL is running and credentials in `settings.py` are correct.
  - Test connection:
    ```bash
    psql -h localhost -U postgres -d event_db
    ```
- **CSRF Token Error**:
  - For testing, add `@csrf_exempt` to views (not for production):
    ```python
    # event_management/views.py
    from django.views.decorators.csrf import csrf_exempt
    from django.utils.decorators import method_decorator

    @method_decorator(csrf_exempt, name='dispatch')
    class EventRegisterView(generics.GenericAPIView):
        ...
    ```
  - Alternatively, include `X-CSRFToken` in Postman requests.
- **ValidationError HTML Page**:
  - If you see an HTML debug page, ensure `views.py` handles exceptions (see `EventRegisterView` in [API Endpoints](#api-endpoints)).
  - Set `DEBUG = False` in `settings.py` for production to return JSON errors.
- **Timezone Issues**:
  - Verify `pytz` is installed (`pip install pytz`).
  - Ensure `USE_TZ = True` in `settings.py`.
  - Use valid timezone strings (e.g., `Asia/Kolkata`, see `pytz.all_timezones`).
- **Event Not Found**:
  - Check the database:
    ```bash
    python manage.py shell
    ```
    ```python
    from event_management.models import Event
    Event.objects.all()
    ```

## Project Structure
```
event_management_system/
├── event_management/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── event_management_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
├── requirements.txt
```

- **models.py**: Defines `Event` and `Attendee` models.
- **serializers.py**: Handles data validation and timezone conversion.
- **services.py**: Business logic for attendee registration.
- **views.py**: API views for CRUD operations.
- **urls.py**: API endpoint routing.
- **settings.py**: Project configuration (database, timezone, etc.).