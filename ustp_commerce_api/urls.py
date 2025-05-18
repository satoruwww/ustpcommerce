from django.urls import path
from .views import (
    api_home,
    protected_view,
    login_or_register,
    UserProfileListCreateView,
    UserProfileDetailView,
    get_users,
    get_user_by_uid,
    get_mock_users,
)

urlpatterns = [
    path('', api_home, name='api_home'),
    path('protected/', protected_view, name='protected_view'),
    path('login/', login_or_register, name='login_or_register'),

    # User APIs
    path('users/', UserProfileListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserProfileDetailView.as_view(), name='user-detail'),
    path('users/uid/<str:uid>/', get_user_by_uid, name='get-user-by-uid'),
    path('users/all/', get_users, name='get_users'),

    # Optional mock users
    path('mock-users/', get_mock_users, name='mock_users'),
]
