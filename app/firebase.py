import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Initialisation de Firebase Admin SDK
cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
firebase_app = firebase_admin.initialize_app(cred)

# Connexion à Firestore
db = firestore.client()
