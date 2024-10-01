import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

load_dotenv()

firebase_credential_path = os.getenv('FIREBASE_CREDENTIAL_PATH')

cred = credentials.Certificate(firebase_credential_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
