from django.contrib import admin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'uid', 'full_name', 'created_at')
    search_fields = ('email', 'full_name', 'uid')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__email', 'bio')
