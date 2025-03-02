from django.urls import path
from .views import api_home, protected_view, login_or_register

urlpatterns = [
    path('', api_home, name='api_home'),
    path('protected/', protected_view, name='protected_view'),
    path('login/', login_or_register, name='login_or_register'),
]
