import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)

load_dotenv()
logging.info(f"start")

private_key = os.getenv("FIREBASE_PRIVATE_KEY")
firebase_credentials = {
    "type": "service_account",
    "project_id": "rattm-78855",
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": (
        private_key.replace("\\\\n", "\n")
        if "\\\\n" in private_key
        else private_key.replace("\\n", "\n")
    ),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("FIREBASE_CERT_URL"),
    "universe_domain": "googleapis.com",
}

# Initialize the Firebase app using the credentials
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

db = firestore.client()
