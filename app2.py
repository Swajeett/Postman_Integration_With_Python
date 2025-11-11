from flask import Flask, jsonify, request
import requests
from threading import Thread
import time

app = Flask(__name__)

# -------------------------------
# Dummy in-memory user database
# -------------------------------
users_db = {}  # Example: { "gaurav@example.com": {"name": "Gaurav", "password": "1234"} }

# -------------------------------
# Home route
# -------------------------------
@app.route('/')
def home():
    return """
    <h2>✅ Flask Auth API is Running!</h2>
    <p>Available Routes:</p>
    <ul>
      <li>POST /api/register — Register new user</li>
      <li>POST /api/login — Login user</li>
    </ul>
    <p>Use Postman with JSON body.</p>
    """

# -------------------------------
# Dummy favicon (prevents 404)
# -------------------------------
@app.route('/favicon.ico')
def favicon():
    return '', 204

# -------------------------------
# REGISTER Endpoint
# -------------------------------
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json(force=True)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Basic validation
        if not all([name, email, password]):
            return jsonify({'error': 'All fields (name, email, password) are required.'}), 400

        if email in users_db:
            return jsonify({'error': 'Email already registered.'}), 409

        # Save user
        users_db[email] = {"name": name, "password": password}
        return jsonify({'message': f'User {name} registered successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -------------------------------
# LOGIN Endpoint
# -------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({'error': 'Email and password are required.'}), 400

        user = users_db.get(email)
        if not user:
            return jsonify({'error': 'User not found.'}), 404

        if user['password'] != password:
            return jsonify({'error': 'Invalid credentials.'}), 401

        return jsonify({'message': f'Welcome back, {user["name"]}!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -------------------------------
# API Test Function
# -------------------------------
def call_api_tests():
    base_url = "http://127.0.0.1:5000/api"

    # 1️⃣ Register test
    print("\n---- Register Test ----")
    register_payload = {"name": "Gaurav", "email": "gaurav@example.com", "password": "1234"}
    r1 = requests.post(f"{base_url}/register", json=register_payload)
    print("Register Response:", r1.text)

    # 2️⃣ Login test
    print("\n---- Login Test ----")
    login_payload = {"email": "gaurav@example.com", "password": "1234"}
    r2 = requests.post(f"{base_url}/login", json=login_payload)
    print("Login Response:", r2.text)

# -------------------------------
# Run Flask Server and Test
# -------------------------------
if __name__ == '__main__':
    def run_server():
        app.run(debug=False, use_reloader=False)

    Thread(target=run_server).start()

    # Wait a bit for server to start
    time.sleep(1)

    # Call API Tests (simulating Postman)
    call_api_tests()
