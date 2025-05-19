from django.http import JsonResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer, CustomUserSerializer,
    ProductSerializer, CustomerSerializer,
    OrderSerializer, OrderItemSerializer,
    CustomTokenObtainPairSerializer
)

from .models import CustomUser, Product, Customer, Order, OrderItem


# ── Registration Endpoint ───────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to register without authentication
def register_user(request):
    """
    POST /api/auth/register/
    Required JSON body: { "email": "...", "full_name": "...", "password": "..." }
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'User registered successfully'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🌐 Welcome message
def api_home(request):
    return JsonResponse({"message": "Welcome to the USTP Commerce API!"})


# 🔒 Firebase auth-protected view (you may remove this later if skipping Firebase)
def protected_view(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    return JsonResponse({
        'message': f'Hello {firebase_user["email"]}, you are authenticated!'
    })


# 🔐 Firebase login/register (you may remove if skipping Firebase)
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


# 📋 List/Create users
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# 🔍 Retrieve/Update/Delete user
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


# 🛍️ API ViewSets for core models
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


# -- JWT login view using your custom serializer --
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
