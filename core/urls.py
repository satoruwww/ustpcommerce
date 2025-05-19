from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    api_home, protected_view, login_or_register,
    UserProfileListCreateView, UserProfileDetailView,
    get_users, get_user_by_uid, get_mock_users,
    ProductViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', api_home),
    path('auth/', login_or_register),
    path('auth/protected/', protected_view),

    path('users/', UserProfileListCreateView.as_view()),
    path('users/<int:pk>/', UserProfileDetailView.as_view()),
    path('users/all/', get_users),
    path('users/uid/<str:uid>/', get_user_by_uid),
    path('mock-users/', get_mock_users),

    path('store/', include(router.urls)),  # CRUD endpoints for products, customers, etc.
]
