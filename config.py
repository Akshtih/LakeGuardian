import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-dev-key-change-in-production'
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS') or 'firebase-credentials.json'
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY') or 'YOUR_GOOGLE_MAPS_API_KEY'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'YOUR_GEMINI_API_KEY'