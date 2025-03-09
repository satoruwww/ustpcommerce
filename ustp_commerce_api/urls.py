from django.urls import path
from .views import (
    get_users,
    api_home, 
    protected_view, 
    login_or_register, 
    UserProfileListCreateView, 
    UserProfileDetailView
)

urlpatterns = [
    path('', api_home, name='api_home'),
    path('protected/', protected_view, name='protected_view'),
    path('login/', login_or_register, name='login_or_register'),
    path('users/', UserProfileListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserProfileDetailView.as_view(), name='user-detail'),
    path('users/',get_users, name='get_users'),
]
