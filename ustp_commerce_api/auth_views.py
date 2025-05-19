from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from ustp_commerce_api.auth_serializers import RegisterSerializer  # ✅ fixed import

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        })
