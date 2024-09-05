#!/usr/bin/env python3
"""session auth module"""

from api.v1.auth.auth import Auth
import uuid


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
