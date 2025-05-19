from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from ustp_commerce_api import auth_urls  # ✅ correct import

def home(request):
    return HttpResponse("Hello, this is the home page!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('core.urls')),
    path('api/auth/', include(auth_urls.urlpatterns)),  # ✅ include actual urlpatterns
]
