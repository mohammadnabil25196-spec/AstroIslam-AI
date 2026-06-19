import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from database import get_db_connection, init_db

app = Flask(__name__)
CORS(app, supports_credentials=True)

openai.api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE")

init_db()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Saari fields bharna zaroori hai!"}), 400
    otp = str(random.randint(100000, 999999))
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (email, password, otp, is_verified) VALUES (?, ?, ?, 0)", (email, password, otp))
        conn.commit()
        return jsonify({"message": "OTP Sent!", "otp_preview": otp}), 200
    except Exception:
        return jsonify({"error": "Email pehle se register hai!"}), 400
    finally:
        conn.close()

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    user_otp = data.get('otp')
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if user and user['otp'] == user_otp:
        conn.execute("UPDATE users SET is_verified = 1 WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Verification Successful!"}), 200
    conn.close()
    return jsonify({"error": "Galt OTP dala hai aapne!"}), 400

@app.route('/api/admin/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, email, status FROM users WHERE status != 'admin'").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users]), 200

@app.route('/api/admin/delete-user', methods=['POST'])
def delete_user():
    data = request.json
    user_id = data.get('id')
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User ko successfully remove kar diya gaya hai!"}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    question = data.get('question', '').strip()
    lang = data.get('lang', 'Hinglish')
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "Pehle login ya register karein!"}), 403
    match = conn.execute("SELECT * FROM knowledge_base WHERE question LIKE ?", (f"%{question}%",)).fetchone()
    if match:
        full_res = f"{match['answer']}\n\n**📜 HAWALA / SOURCE:** {match['hawala']}"
        conn.close()
        return jsonify({"response": full_res, "source": "Custom DB"}), 200
    try:
        system_prompt = f"You are AstroIslam AI. Only answer Cosmology & Quranic Science in {lang}. Strict rule: You must always add an authentic 'HAWALA / SOURCE' (like Quran verse, Hadith chapter, or Mufti context) at the very bottom of the answer."
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]
        )
        response_text = completion.choices.message.content
        conn.close()
        return jsonify({"response": response_text, "source": "OpenAI API"}), 200
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
