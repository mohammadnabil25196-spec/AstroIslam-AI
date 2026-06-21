from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/api/login', methods=['POST'])
def login():
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(port=5000)
