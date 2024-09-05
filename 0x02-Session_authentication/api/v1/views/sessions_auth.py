#!/usr/bin/env python3
"""session auth module"""

from flask import request, jsonify
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth


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
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = SessionAuth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie('my_session_id', session_id)
    return response
