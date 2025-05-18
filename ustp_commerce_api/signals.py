from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
from .firebase_config import add_user_to_firestore

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, _ = UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=UserProfile)
def push_user_to_firestore(sender, instance, **kwargs):
    print("📡 SIGNAL: UserProfile post_save triggered")
    try:
        add_user_to_firestore(instance)
    except Exception as e:
        print("❌ Firestore sync failed:", e)
