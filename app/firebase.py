import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialisation de Firebase Admin SDK
cred = credentials.Certificate("service.json")
firebase_app = firebase_admin.initialize_app(cred)

# Connexion à Firestore
db = firestore.client()
