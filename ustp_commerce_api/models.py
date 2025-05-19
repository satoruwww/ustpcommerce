from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

# Custom user model
class CustomUser(AbstractUser):
    uid = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email or self.username


# UserProfile model with user relation using AUTH_USER_MODEL to avoid import issues
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# Import Firestore sync function here to avoid circular imports
from .firebase_config import add_user_to_firestore


# Automatically create UserProfile when a new CustomUser is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        transaction.on_commit(lambda: add_user_to_firestore(profile))


# Firestore sync when UserProfile is saved
@receiver(post_save, sender=UserProfile)
def save_user_to_firestore(sender, instance, **kwargs):
    print("📡 SIGNAL: UserProfile post_save triggered")
    transaction.on_commit(lambda: add_user_to_firestore(instance))
