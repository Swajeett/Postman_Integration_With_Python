from flask import Flask, jsonify, request
import requests
from threading import Thread
import time

app = Flask(__name__)

# -------------------------------
# Home route (prevents 404 for '/')
# -------------------------------
@app.route('/')
def home():
    return """
    <h2>✅ Flask API is running!</h2>
    <p>Try sending a POST request to <b>/api/greet</b> with JSON:</p>
    <pre>{
      "name": "Gaurav"
    }</pre>
    """

# -------------------------------
# Dummy favicon (prevents 404)
# -------------------------------
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content response


# -------------------------------
# Flask API Endpoint
# -------------------------------
@app.route('/api/greet', methods=['POST'])
def greet():
    try:
        data = request.get_json(force=True)
        name = data.get('name', 'User')
        return jsonify({'message': f'Hello, {name}!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# -------------------------------
# Function to Test the API (Postman-style)
# -------------------------------
def call_api():
    url = "http://127.0.0.1:5000/api/greet"
    payload = {"name": "Gaurav"}  # ✅ your JSON body
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("\nResponse from API:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error while calling API:", e)


# -------------------------------
# Run Flask + Test API
# -------------------------------
if __name__ == '__main__':
    # Run Flask server in background
    def run_server():
        app.run(debug=False, use_reloader=False)

    Thread(target=run_server).start()

    # Wait for server to start
    time.sleep(1)

    # Call the API once Flask is up
call_api()