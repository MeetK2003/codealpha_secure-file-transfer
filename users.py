from flask_login import UserMixin

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "password123", "role": "user"}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]["role"]

def load_user(username):
    if username not in users:
        return None
    return User(username)
