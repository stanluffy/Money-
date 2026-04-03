=============================

SIMPLE INCOME APP (TASK + ADS MODEL)

Earn via: referrals + simple tasks + ads

Backend: Flask API

=============================

from flask import Flask, request, jsonify from flask_cors import CORS import sqlite3 import hashlib

app = Flask(name) CORS(app)

=============================

DATABASE SETUP

=============================

def init_db(): conn = sqlite3.connect('app.db') c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    balance REAL DEFAULT 0,
    referral_code TEXT
)''')

conn.commit()
conn.close()

init_db()

=============================

HELPER

=============================

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()

=============================

REGISTER

=============================

@app.route('/register', methods=['POST']) def register(): data = request.json username = data['username'] password = hash_password(data['password'])

conn = sqlite3.connect('app.db')
c = conn.cursor()

try:
    referral_code = username + "123"
    c.execute("INSERT INTO users (username, password, referral_code) VALUES (?, ?, ?)",
              (username, password, referral_code))
    conn.commit()
    return jsonify({'message': 'Registered successfully'})
except:
    return jsonify({'error': 'User already exists'})

=============================

LOGIN

=============================

@app.route('/login', methods=['POST']) def login(): data = request.json username = data['username'] password = hash_password(data['password'])

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
user = c.fetchone()

if user:
    return jsonify({'message': 'Login success', 'balance': user[3]})
else:
    return jsonify({'error': 'Invalid credentials'})

=============================

COMPLETE TASK (earn money)

=============================

@app.route('/task', methods=['POST']) def task(): data = request.json username = data['username']

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("UPDATE users SET balance = balance + 0.1 WHERE username=?", (username,))
conn.commit()

return jsonify({'message': 'Task completed. Earned $0.1'})

=============================

REFERRAL BONUS

=============================

@app.route('/referral', methods=['POST']) def referral(): data = request.json ref_code = data['referral_code']

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("UPDATE users SET balance = balance + 1 WHERE referral_code=?", (ref_code,))
conn.commit()

return jsonify({'message': 'Referral bonus added'})

=============================

RUN SERVER

=============================

if name == 'main': app.run(debug=True)

=============================

HOW TO DEPLOY (RENDER)

=============================

1. Create requirements.txt:

flask

flask-cors

gunicorn



2. Start command:

gunicorn app:app



=============================

HOW YOU MAKE MONEY

=============================

1. Add ads (AdMob for mobile)

2. Charge withdrawals fee

3. Promote referral system

4. Sell premium upgrade

=============================

NEXT STEP (IMPORTANT)

=============================

Tell ChatGPT:

"Create Android app UI for this API"

and you'll get APK version
