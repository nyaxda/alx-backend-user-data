#!/usr/bin/env python3
"""session auth module"""

from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Handles user login and session creation"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    session_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)
    return response
