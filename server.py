import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from database import get_db_connection, init_db

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Admin Config
ADMIN_EMAIL = "admin@astroislam.com"
ADMIN_PASS = "admin123"

openai.api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE")
init_db()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if email == ADMIN_EMAIL and password == ADMIN_PASS:
        return jsonify({"success": True, "role": "admin"}), 200
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
    conn.close()
    if user: return jsonify({"success": True, "role": "user"}), 200
    return jsonify({"error": "Galt details!"}), 401

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    question = data.get('question', '').strip()
    
    # Admin Bypass
    if email == ADMIN_EMAIL and password == ADMIN_PASS:
        pass 
    else:
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if not user: return jsonify({"error": "Pehle login karein!"}), 403

    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])
        return jsonify({"response": completion.choices[0].message.content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
