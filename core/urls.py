from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    api_home, protected_view, login_or_register, register_user,
    UserProfileListCreateView, UserProfileDetailView,
    get_users, get_user_by_uid, get_mock_users,
    ProductViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet,
    CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', api_home, name='api-home'),

    # Auth endpoints
    path('auth/', login_or_register, name='login-or-register'),  
    path('auth/register/', register_user, name='register'),      
    path('auth/protected/', protected_view, name='protected'),   
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  

    # User profile endpoints
    path('users/', UserProfileListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserProfileDetailView.as_view(), name='user-detail'),
    path('users/all/', get_users, name='get-users'),
    path('users/uid/<str:uid>/', get_user_by_uid, name='get-user-by-uid'),

    # Mock users endpoint
    path('mock-users/', get_mock_users, name='mock-users'),

    # Store API endpoints via router
    path('store/', include(router.urls)),
]
