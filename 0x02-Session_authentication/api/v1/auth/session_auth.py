#!/usr/bin/env python3
"""session auth module"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User
from flask import request, jsonify
from api.v1.views import app_views


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get a user ID from a session ID"""
        if session_id is None or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Get a user
        Returns: a User instance
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

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
