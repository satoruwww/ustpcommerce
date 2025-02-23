from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # Import HttpResponse for testing

def home(request):
    return HttpResponse("Hello, this is the home page!")  # Simple homepage response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Keep the homepage
    path('api/', include('ustp_commerce_api.urls')),  # ✅ Add this to include API routes
]
