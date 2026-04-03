WORKING FLASK APP (RENDER READY)

from flask import Flask, request, jsonify from flask_cors import CORS import sqlite3 import hashlib import os

app = Flask(name) CORS(app)

=============================

DATABASE SETUP

=============================

def init_db(): conn = sqlite3.connect('app.db') c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    balance REAL DEFAULT 0
)''')

conn.commit()
conn.close()

init_db()

=============================

HELPER

=============================

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()

=============================

HOME ROUTE (IMPORTANT)

=============================

@app.route('/') def home(): return "App is running ✅"

=============================

REGISTER

=============================

@app.route('/register', methods=['POST']) def register(): data = request.get_json() username = data.get('username') password = hash_password(data.get('password'))

conn = sqlite3.connect('app.db')
c = conn.cursor()

try:
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    return jsonify({'message': 'Registered successfully'})
except:
    return jsonify({'error': 'User already exists'})

=============================

LOGIN

=============================

@app.route('/login', methods=['POST']) def login(): data = request.get_json() username = data.get('username') password = hash_password(data.get('password'))

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
user = c.fetchone()

if user:
    return jsonify({'message': 'Login success', 'balance': user[3]})
else:
    return jsonify({'error': 'Invalid credentials'})

=============================

TASK (EARN MONEY)

=============================

@app.route('/task', methods=['POST']) def task(): data = request.get_json() username = data.get('username')

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("UPDATE users SET balance = balance + 0.1 WHERE username=?", (username,))
conn.commit()

return jsonify({'message': 'Task completed', 'earned': 0.1})

=============================

CHECK BALANCE

=============================

@app.route('/balance', methods=['POST']) def balance(): data = request.get_json() username = data.get('username')

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("SELECT balance FROM users WHERE username=?", (username,))
user = c.fetchone()

if user:
    return jsonify({'balance': user[0]})
else:
    return jsonify({'error': 'User not found'})

=============================

RUN (RENDER READY)

=============================

if name == 'main': port = int(os.environ.get("PORT", 5000)) app.run(host='0.0.0.0', port=port)

=============================

REQUIREMENTS.TXT

=============================

flask

flask-cors

gunicorn

=============================

RENDER START COMMAND

=============================

gunicorn app:app
