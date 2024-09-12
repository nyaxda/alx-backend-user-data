#!/usr/bin/env python3
"""app module"""

from flask import (Flask, jsonify, request, abort,
                   make_response, url_for, redirect)
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """basic Flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "user already exists"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Login a user and create a session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logs out a user"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            response = make_response(redirect(url_for('home')))
            response.delete_cookie('session_id')
            return response
    return abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Get the user profile"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": f"{user.email}"})
    return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
