from flask import Flask
from config import Config
import firebase_admin
from firebase_admin import credentials
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)

# Create necessary directories
os.makedirs('instance', exist_ok=True)

# Initialize Firebase
try:
    cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
    firebase_app = firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized
    pass

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes, models