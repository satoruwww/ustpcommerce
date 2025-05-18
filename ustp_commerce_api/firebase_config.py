# firebase_config.py

import firebase_admin
from firebase_admin import credentials, firestore

# ✅ Only initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("D:/ustpcommerce/ustp_commerce_api/firebase_config.json")  # ✅ Update path if needed
    firebase_admin.initialize_app(cred)

# ✅ Firestore client
firebase_db = firestore.client()

# ✅ Function to add or update user in Firestore
def add_user_to_firestore(user_profile):
    from .models import UserProfile  # 🔁 Avoid circular imports

    if not isinstance(user_profile, UserProfile):
        print("❌ Not a UserProfile instance:", type(user_profile))
        raise TypeError("Expected a UserProfile instance")

    user = user_profile.user  # Get related CustomUser

    user_data = {
        "uid": user.uid,
        "email": user.email,
        "fullName": user.full_name,
        "bio": user_profile.bio,
        "createdAt": user.created_at.isoformat() if user.created_at else None
    }

    print("🟡 DEBUG: Writing to Firestore:", user_data)

    try:
        firebase_db.collection("users").document(user.uid).set(user_data, merge=True)
        print("✅ Firestore write successful.")
    except Exception as e:
        print("❌ Error writing to Firestore:", e)
