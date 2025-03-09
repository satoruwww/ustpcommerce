from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProfile
from .serializers import UserProfileSerializer

# Public API home
def api_home(request):
    return JsonResponse({"message": "Welcome to the USTP Commerce API!"})

# Protected View
def protected_view(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    return JsonResponse({'message': f'Hello {firebase_user["email"]}, you are authenticated!'})

# Login or Register View
def login_or_register(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    uid = firebase_user['uid']
    email = firebase_user['email']

    user, created = UserProfile.objects.get_or_create(uid=uid, defaults={
        'email': email,
        'full_name': firebase_user.get('name', 'Anonymous')
    })

    return JsonResponse({'message': 'Login successful', 'user': {
        'email': user.email,
        'full_name': user.full_name,
        'created': user.created_at
    }})

# API View for listing and creating user profiles
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# API View for retrieving, updating, and deleting a specific user profile
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# API function-based view to get all users from the database
@api_view(['GET'])
def get_users(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)

# Simple function to return mock users
def get_mock_users(request):
    data = [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Doe"},
    ]
    return JsonResponse(data, safe=False)
