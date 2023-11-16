#!/usr/bin/env python3

"""Basic Flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


AUTH = Auth()


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Register user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/session', methods=['POST'], strict_slash=False)
def login():
    """Log in"""

    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login():
        session_id = create_session()
        session['session_id'] = session_id

    else:
        abort()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
