from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# import the logging library
import logging

from .serializers import *
from .models import *
# Get an instance of a logger
logger = logging.getLogger('event_manager')

@swagger_auto_schema(
    order=1,
    method='post',
    operation_description='Registers a new user.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password', 'email'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
    },
)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    API endpoint for registering a new user.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response containing access_token, refresh_token, and user information upon successful registration.

    Raises:
        Exception: If username or email is already taken.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Check if username or email is already taken
    if CustomUser.objects.filter(username=username).exists():
        raise Exception('Username is already taken.')
    elif CustomUser.objects.filter(email=email).exists():
        raise Exception('Email is already taken.')

    # Create new user
    user = CustomUser(username=username, email=email)
    user.set_password(password)
    user.save()

    return Response({"success": f"User {user.username} created."}, status=201)

@swagger_auto_schema(
    order=2,
    method='post',
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
        }
    ),
    responses={
        200: openapi.Response('User logged in successfully'),
        400: openapi.Response('Bad request'),
        401: openapi.Response('Unauthorized')
    },
    operation_description="Log in an existing user."
)
@csrf_exempt
@api_view(["POST"])
def login_user(request):
    """
    Authenticate a user and return an access token and a refresh token.

    Args:
        request (HttpRequest): The request object sent by the client.

    Returns:
        A JsonResponse containing the access token and refresh token.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Please provide both username and password."}, status=400
        )    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({"error": "Invalid username or password."}, status=401)

    access_token = RefreshToken.for_user(user).access_token
    refresh_token = RefreshToken.for_user(user)
    return Response(
        {"access_token": str(access_token), "refresh_token": str(refresh_token)}
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """
    Logs out the currently authenticated user.
    """
    try:
        access_token = request.data.get('refresh_token')
       
        token = RefreshToken(access_token)
        token.blacklist()
        logout(request)
        return Response({'success': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.warning(f'Error: {e}')
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_event(request):
    """
    API endpoint a user to create a new event.
    
    Parameters:
    -----------
    request: Request
        Django request object
        
    Input:
    ------
    The request should contain a JSON body with the following fields:
        - name: str, the name of the event
        - description: str, the description of the event
        - start_date: datetime, the start date and time of the event in the format yyyy-mm-ddThh:mm:ssZ
        - end_date: datetime, the end date and time of the event in the format yyyy-mm-ddThh:mm:ssZ
        - max_capacity: int, the maximum capacity of the event
        - attendees: list of str, the usernames of the attendees
        
    Output:
    -------
    Returns a JSON response with the serialized event object.
    """
    # get owner based on authenticated user
    owner = request.user
    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(owner=owner)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
def fetch_user_events(request):
    """
    API endpoint for getting all events created by the current user.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response containing a list of all events created by the current user.
    """
    events = Event.objects.filter(owner=request.user)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    order=3,
    method='get',
    operation_description='Get list of events',
    responses={200: openapi.Response('List of events')},
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_events(request):
    """
    API endpoint to list all events.

    Parameters:
    -----------
    request: Request
        Django request object

    Input:
    ------
    status: str (optional)
        Filter events by status (upcoming, ongoing, past).
    date: str (optional)
        Filter events by date (YYYY-MM-DD).

    Output:
    -------
    Returns a JSON response with a list of serialized event objects.
    """
    status = request.query_params.get('status')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Filter events by status
    if status:
        today = datetime.now().date()
        if status == 'upcoming':
            events = Event.objects.filter(start_date__gte=today)
        elif status == 'ongoing':
            events = Event.objects.filter(start_date__lte=today, end_date__gte=today)
        elif status == 'past':
            events = Event.objects.filter(end_date__lt=today)
        else:
            return Response({'error': 'Invalid status filter'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        events = Event.objects.all()

    # Filter events by date
    if start_date:
        try:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            events = events.filter(start_date__date=date_obj)
        except ValueError:
            return Response({'error': 'Invalid date filter (use YYYY-MM-DD format)'}, status=status.HTTP_400_BAD_REQUEST)
    if end_date:
        try:
            date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            events = events.filter(end_date__date=date_obj)
        except ValueError:
            return Response({'error': 'Invalid date filter (use YYYY-MM-DD format)'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def edit_event(request, event_id):
    """
    Edit an existing event
    
    Args:
        request (HttpRequest): The request object containing the new event data
        event_id (int): The ID of the event to edit
        
    Returns:
        JSON object containing the updated event data
        
    Raises:
        Http404: If the event with the given ID does not exist
        PermissionDenied: If the authenticated user did not create the event
    """

    try:        
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404('Event does not exist.')
    
    # Check if the authenticated user is the owner of the event
    if event.owner != request.user:
        raise PermissionDenied('You are not the owner of this event.')
    
    serializer = EditEventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Event updated successfully.', 'data': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_event(request, event_id):
    """
    Register the authenticated user to an event.

    Args:
        request: HttpRequest object representing the current request.
        event_id: The ID of the event to register to.

    Returns:
        A JSON response containing the updated event data on success, or a
        404 error response if the event was not found, or a 400 error response
        if the authenticated user is already registered to the event.
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    # Check that the event is in the future
    if event.start_date < datetime.now(timezone.utc):
        return Response({"error": "You can only register for future events."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the user is already registered for the event
    if request.user in event.attendees.all():
        return Response({'error': 'You are already registered to this event.'}, status=status.HTTP_400_BAD_REQUEST)
    # Check if the event has already reached its maximum capacity
    if event.max_capacity and event.attendees.count() >= event.max_capacity:
        return Response({"success": False, "error": "Event has reached its maximum capacity"})
    
    # Add the user as an attendee to the event
    user = request.user
    event.attendees.add(user)

    # Register the user for the event
    serializer = RegisterEventSerializer(instance=event, data={"attendees": [request.user.id]}, partial=True, context={'request': request})

    if serializer.is_valid():
        # Add the user as an attendee to the event
        serializer.save()
        return JsonResponse({"success": True, 'messagge': 'user registred for the event'})
    else:
        return JsonResponse({"success": False, "error": serializer.errors})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unregister_event(request, event_id):
    """
    Unregister the authenticated user from an event.

    Args:
        request: HttpRequest object representing the current request.
        event_id: The ID of the event to unregister from.

    Returns:
        A JSON response containing the updated event data on success, or a
        404 error response if the event was not found, or a 400 error response
        if the authenticated user is not registered to the event.
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    # Check that the event is in the future
    if event.start_date < datetime.now(timezone.utc):
        return Response({"error": "You can only unregister for future events."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Unregister the user from the event
        event = Event.objects.get(id=event_id)
        attendees = event.attendees.all()
        if request.user not in attendees:
            return JsonResponse({"success": True, "error": "User is not registered for this event"})
        event.attendees.remove(request.user)
        event.save()
        return JsonResponse({"success": True, "messagge": "user unregistred for the event"})
    except Exception as e:
        return JsonResponse({"success": False, "error": e })

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
