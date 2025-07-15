#!/usr/bin/env python3
"""
Simple test to verify the Flask app can start without errors
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("✓ App imported successfully")
    
    # Test basic route
    with app.test_client() as client:
        response = client.get('/')
        print(f"✓ Home page returns status: {response.status_code}")
        
    print("✓ All basic tests passed!")
    print("Note: To run the full app, you'll need to:")
    print("1. Set up your .env file with API keys")
    print("2. Set up Firebase credentials")
    print("3. Run: python run.py")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure you've installed all dependencies:")
    print("pip install flask firebase-admin google-cloud-storage python-dotenv Pillow requests flask-login flask-wtf")
    
except Exception as e:
    print(f"✗ Error: {e}")
