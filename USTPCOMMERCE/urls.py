from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is the home page!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Include core app API routes (assuming core/urls.py exists)
    path('api/', include('core.urls')),

    # Include auth routes from core.auth_urls.py properly by string path
    path('api/auth/', include('core.auth_urls')),
]
