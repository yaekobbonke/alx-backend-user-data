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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def session() -> str:
    """ Credentials validation """

    email = request.form.get('email')
    password = request.form.get('password')

    res = AUTH.valid_login(email, password)
    if res:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ logout
    """
    session_cookie = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_cookie)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """User profile
    """
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie)
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Get reset password token
    """
    email = request.form.get('email')
    try:
        new_token = get_reset_password_token(email)
        if new_token:
            return {"email": email, "reset_token": new_token}
        else:
            abort(403)
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update password end-point
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        update_password('reset_token')
        return {"email": email, "message": "Password updated"}, 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
