from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

db = sqlite3.connect(':memory:', check_same_thread=False)
db.row_factory = sqlite3.Row


def init_db():
    """Initialize the database with the users table."""
    db.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            last_login TIMESTAMP
        )
    ''')
    db.commit()

@app.before_request
def initialize_database():
    """
    Initialize the database before the first request.
    Since before_first_request was removed in Flask 2.3, this is a workaround.
    """
    app.before_request_funcs[None].remove(initialize_database)

    init_db()

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    
    Request JSON should contain 'name', 'email', and 'password'.
    Returns the created user with a hashed password.
    """
    user_data = request.json
    hashed_password = generate_password_hash(user_data['password'])

    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    ''', (user_data['name'], user_data['email'], hashed_password))
    db.commit()
    user_id = cursor.lastrowid
    user_data['id'] = user_id
    user_data['password'] = hashed_password
    
    return jsonify(user_data), 201

@app.route('/users/<email>', methods=['GET'])
def get_user(email):
    """
    Retrieve a user by email.
    
    Returns the user details if found, otherwise returns a 404 error.
    """
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(dict(user))

@app.route('/users/<email>', methods=['PUT'])
def update_user(email):
    """
    Update a user's details by email.
    
    Request JSON should contain 'name', 'email', and optionally 'password'.
    Returns the updated user details if successful, otherwise returns a 404 error.
    """
    user_data = request.json
    if 'password' in user_data:
        user_data['password'] = generate_password_hash(user_data['password'])

    cursor = db.cursor()
    cursor.execute('''
        UPDATE users
        SET name = ?, email = ?, password = ?
        WHERE email = ?
    ''', (user_data['name'], user_data['email'], user_data['password'], email))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user_data)

@app.route('/users/<email>', methods=['DELETE'])
def delete_user(email):
    """
    Delete a user by email.
    
    Returns a 204 status code if successful, otherwise returns a 404 error.
    """
    cursor = db.cursor()
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({'error': 'User not found'}), 404
    
    return '', 204

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user by email and password.
    
    Request JSON should contain 'email' and 'password'.
    Returns a success message and user details if successful, otherwise returns a 401 error.
    """
    login_data = request.json
    email = login_data['email']
    password = login_data['password']
    
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    if user is None or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Update last_login timestamp
    db.execute('UPDATE users SET last_login = ? WHERE email = ?', (datetime.now(), email))
    db.commit()
    
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    return jsonify({'message': 'Login successful', 'user': dict(user)})

if __name__ == '__main__':
    app.run(debug=True)