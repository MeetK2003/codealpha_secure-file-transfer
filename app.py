from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from users import load_user, User
from routes import routes

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "password123", "role": "user"}
}

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(username):
    return load_user(username)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username not in users or users[username]["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    user = User(username)
    login_user(user)
    return jsonify({"message": f"Welcome, {username}!"})

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})

@app.route('/')
def home():
    return 'Hello, Secure File Transfer'

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
