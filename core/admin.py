from django.contrib import admin
from .models import (
    CustomUser,
    Product,
    Category,
    UserProfile,
    Customer,
    Order,
    OrderItem,
)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'uid', 'is_staff', 'is_active', 'created_at')
    search_fields = ('email', 'full_name', 'uid')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__email', 'bio')

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
