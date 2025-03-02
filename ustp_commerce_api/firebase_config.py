import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('ustp_commerce_api/firebase_config.json')
firebase_admin.initialize_app(cred)
