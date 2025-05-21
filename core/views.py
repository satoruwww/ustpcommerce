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


# ── Registration Endpoint ───────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'User registered successfully'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_home(request):
    return Response({"message": "Welcome to the USTP Commerce API!"})


@api_view(['GET'])
def protected_view(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({
        'message': f'Hello {firebase_user["email"]}, you are authenticated!'
    })


@api_view(['GET'])
def login_or_register(request):
    firebase_user = getattr(request, 'firebase_user', None)
    if not firebase_user:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    uid = firebase_user['uid']
    email = firebase_user['email']
    user, created = CustomUser.objects.get_or_create(
        uid=uid,
        defaults={
            'email': email,
            'full_name': firebase_user.get('name', 'Anonymous')
        }
    )
    return Response({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'uid': user.uid,
            'email': user.email,
            'full_name': user.full_name,
            'created': user.created_at
        }
    })


class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_by_uid(request, uid):
    try:
        user = CustomUser.objects.get(uid=uid)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_mock_users(request):
    data = [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Doe"},
    ]
    return Response(data)


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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
