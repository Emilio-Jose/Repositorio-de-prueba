from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
DB = 'usuarios.db'

def get_db():
    return sqlite3.connect(DB)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nombre = data['nombre']
    pwd = data['password']
    pw_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
    conn = get_db()
    conn.execute('INSERT INTO users (nombre, password_hash) VALUES (?, ?)', (nombre, pw_hash))
    conn.commit()
    conn.close()
    return jsonify(msg="Usuario registrado"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    nombre = data['nombre']
    pwd = data['password']
    conn = get_db()
    user = conn.execute('SELECT password_hash FROM users WHERE nombre = ?', (nombre,)).fetchone()
    conn.close()
    if user and bcrypt.check_password_hash(user[0], pwd):
        return jsonify(msg="Login exitoso")
    return jsonify(msg="Usuario o clave inválidos"), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500)
