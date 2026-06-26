from flask import Flask, request, jsonify, send_from_directory
import os
import sqlite3

app = Flask(__name__)

# डेटाबेस शुरू करें और टेबल बनाएं
def init_db():
    conn = sqlite3.connect('astroislam.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS info_table (id INTEGER PRIMARY KEY, content TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/api/login', methods=['POST'])
def login():
    return jsonify({"success": True})

@app.route('/api/add-info', methods=['POST'])
def add_info():
    data = request.json
    info_text = data.get('info')
    if not info_text:
        return jsonify({"success": False, "message": "No content provided"})
    
    conn = sqlite3.connect('astroislam.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO info_table (content) VALUES (?)", (info_text,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').lower()
    
    conn = sqlite3.connect('astroislam.db')
    cursor = conn.cursor()
    # डेटाबेस में सर्च करें
    cursor.execute("SELECT content FROM info_table WHERE content LIKE ?", ('%' + user_msg + '%',))
    result = cursor.fetchone()
    conn.close()
    
    answer = result if result else "I do not have information about this yet."
    return jsonify({"reply": answer})

if __name__ == '__main__':
    app.run(port=5000)
