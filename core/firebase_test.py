from firebase_admin import initialize_app
from firebase_config import cred

initialize_app(cred)

print("✅ Firebase connected successfully!")
