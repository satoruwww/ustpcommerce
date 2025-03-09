from firebase_admin import initialize_app
from ustp_commerce_api.firebase_config import cred

initialize_app(cred)

print("✅ Firebase connected successfully!")
