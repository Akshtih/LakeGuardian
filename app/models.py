from flask_login import UserMixin
from app import login_manager
from firebase_admin import auth, firestore

db = firestore.client()

class User(UserMixin):
    def __init__(self, uid, email, display_name):
        self.id = uid
        self.email = email
        self.display_name = display_name
        
    @staticmethod
    def get_by_email(email):
        try:
            user = auth.get_user_by_email(email)
            return User(
                uid=user.uid,
                email=user.email,
                display_name=user.display_name
            )
        except:
            return None

@login_manager.user_loader
def load_user(user_id):
    try:
        user = auth.get_user(user_id)
        return User(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name
        )
    except:
        return None