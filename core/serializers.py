from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import CustomUser, Product, Customer, Order, OrderItem


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'uid', 'email', 'full_name', 'is_active', 'is_staff', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name']
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True, read_only=True, source='orderitem_set'
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_ordered', 'total_price', 'items']


# Custom JWT Token Serializer to authenticate via email instead of username
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here if needed
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email is None or password is None:
            raise serializers.ValidationError('Email and password are required')

        # Authenticate user by email and password
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        # Call parent to get token data
        data = super().validate({'username': email, 'password': password})
        return data
