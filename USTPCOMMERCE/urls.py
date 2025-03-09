from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse 

def home(request):
    return HttpResponse("Hello, this is the home page!")  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Keep the homepage
    path('api/', include('ustp_commerce_api.urls')),  # Include API routes
]
