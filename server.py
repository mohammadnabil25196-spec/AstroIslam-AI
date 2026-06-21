import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from database import init_db

app = Flask(__name__)
CORS(app)
init_db()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
