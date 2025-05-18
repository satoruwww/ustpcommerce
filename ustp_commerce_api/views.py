from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import CustomUserSerializer  # Fixed import

# 🌐 API welcome message
def api_home(request):
    return JsonResponse({"message": "Welcome to the USTP Commerce API!"})

# 🔒 Auth-protected view
def protected_view(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    return JsonResponse({
        'message': f'Hello {firebase_user["email"]}, you are authenticated!'
    })

# 🔐 Firebase login/register
def login_or_register(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    uid = firebase_user['uid']
    email = firebase_user['email']

    user, created = CustomUser.objects.get_or_create(
        uid=uid,
        defaults={
            'email': email,
            'full_name': firebase_user.get('name', 'Anonymous')
        }
    )

    return JsonResponse({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'uid': user.uid,
            'email': user.email,
            'full_name': user.full_name,
            'created': user.created_at
        }
    })

# 📋 List/Create users (class-based)
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# 🔍 Retrieve/Update/Delete user by ID
class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# 🧾 Get all users (function-based)
@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

# 🔎 Get user by Firebase UID
@api_view(['GET'])
def get_user_by_uid(request, uid):
    try:
        user = CustomUser.objects.get(uid=uid)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

# 🧪 Mock test users
def get_mock_users(request):
    data = [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Doe"},
    ]
    return JsonResponse(data, safe=False)
