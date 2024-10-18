# users/firebase.py

import firebase_admin
from firebase_admin import credentials, firestore 

cred = credentials.Certificate('/home/diredi/Desktop/github/roy-realm/roy/users/json/roy-realm-firebase-adminsdk-gbxhz-17f94e8aa2.json')
firebase_admin.initialize_app(cred)


# Initialize Firestore Database
db = firestore.client()