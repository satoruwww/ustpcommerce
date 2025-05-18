from django.contrib import admin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'uid', 'full_name', 'created_at')
    search_fields = ('username', 'email', 'full_name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')
