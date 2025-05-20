from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from ustp_commerce_api import auth_urls  # make sure auth_urls.py exists with urlpatterns inside

def home(request):
    return HttpResponse("Hello, this is the home page!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('core.urls')),  # include core app API routes
    path('api/auth/', include(auth_urls)),  # include auth routes correctly
]
