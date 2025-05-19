from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# 🏠 Homepage view
def home(request):
    return HttpResponse("Hello, this is the home page!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),               # Homepage
    path('api/', include('core.urls')),        # API endpoints from core app
]
