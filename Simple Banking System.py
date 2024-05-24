pip install Flask gradio requests

import threading
from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import gradio as gr
import requests

app = Flask(__name__)

DATABASE = 'banking_system.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Invalid registration data'}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Invalid login data'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        return jsonify({'message': 'Login successful', 'balance': user[3]}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    sender_username = data.get('sender_username')
    sender_password = data.get('sender_password')
    receiver_username = data.get('receiver_username')
    amount = data.get('amount')

    if not sender_username or not sender_password or not receiver_username or not amount:
        return jsonify({'message': 'Invalid transfer data'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (sender_username,))
    sender = cursor.fetchone()

    if not sender or not check_password_hash(sender[2], sender_password):
        conn.close()
        return jsonify({'message': 'Invalid sender credentials'}), 401

    if sender[3] < amount:
        conn.close()
        return jsonify({'message': 'Insufficient balance'}), 402

    cursor.execute("UPDATE users SET balance=balance-? WHERE id=?", (amount, sender[0]))
    cursor.execute("UPDATE users SET balance=balance+? WHERE username=?", (amount, receiver_username))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Transfer successful'}), 200

@app.route('/balance', methods=['POST'])
def check_balance():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Invalid data'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        return jsonify({'message': 'Balance check successful', 'balance': user[3]}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

def run_flask():
    app.run(debug=False)

# Start Flask in a separate thread
threading.Thread(target=run_flask).start()

API_URL = 'http://127.0.0.1:5000'

def register(username, password):
    response = requests.post(f'{API_URL}/register', json={'username': username, 'password': password})
    return response.json()['message']

def login(username, password):
    response = requests.post(f'{API_URL}/login', json={'username': username, 'password': password})
    result = response.json()
    return result['message'], str(result.get('balance', ''))

def transfer(sender_username, sender_password, receiver_username, amount):
    response = requests.post(f'{API_URL}/transfer', json={
        'sender_username': sender_username,
        'sender_password': sender_password,
        'receiver_username': receiver_username,
        'amount': float(amount)
    })
    return response.json()['message']

def check_balance(username, password):
    response = requests.post(f'{API_URL}/balance', json={'username': username, 'password': password})
    result = response.json()
    return result['message'], str(result.get('balance', ''))

register_interface = gr.Interface(fn=register, inputs=[gr.inputs.Textbox(label="Username"), gr.inputs.Textbox(label="Password", type="password")], outputs="text")
login_interface = gr.Interface(fn=login, inputs=[gr.inputs.Textbox(label="Username"), gr.inputs.Textbox(label="Password", type="password")], outputs=["text", "text"])
transfer_interface = gr.Interface(fn=transfer, inputs=[gr.inputs.Textbox(label="Sender Username"), gr.inputs.Textbox(label="Sender Password", type="password"), gr.inputs.Textbox(label="Receiver Username"), gr.inputs.Textbox(label="Amount")], outputs="text")
balance_interface = gr.Interface(fn=check_balance, inputs=[gr.inputs.Textbox(label="Username"), gr.inputs.Textbox(label="Password", type="password")], outputs=["text", "text"])

# Launch Gradio interfaces
register_interface.launch(share=True)
login_interface.launch(share=True)
transfer_interface.launch(share=True)
balance_interface.launch(share=True)





import gradio as gr
import requests

API_URL = 'http://127.0.0.1:5000'

def register(username, password):
    response = requests.post(f'{API_URL}/register', json={'username': username, 'password': password})
    return response.json()['message']

def login(username, password):
    response = requests.post(f'{API_URL}/login', json={'username': username, 'password': password})
    result = response.json()
    return result['message'], str(result.get('balance', ''))

def transfer(sender_username, sender_password, receiver_username, amount):
    response = requests.post(f'{API_URL}/transfer', json={
        'sender_username': sender_username,
        'sender_password': sender_password,
        'receiver_username': receiver_username,
        'amount': float(amount)
    })
    return response.json()['message']

def check_balance(username, password):
    response = requests.post(f'{API_URL}/balance', json={'username': username, 'password': password})
    result = response.json()
    return result['message'], str(result.get('balance', ''))

register_interface = gr.Interface(fn=register, inputs=["text", "password"], outputs="text")
login_interface = gr.Interface(fn=login, inputs=["text", "password"], outputs=["text", "text"])
transfer_interface = gr.Interface(fn=transfer, inputs=["text", "password", "text", "text"], outputs="text")
balance_interface = gr.Interface(fn=check_balance, inputs=["text", "password"], outputs=["text", "text"])

if __name__ == '__main__':
    register_interface.launch(share=True)
    login_interface.launch(share=True)
    transfer_interface.launch(share=True)
    balance_interface.launch(share=True)

