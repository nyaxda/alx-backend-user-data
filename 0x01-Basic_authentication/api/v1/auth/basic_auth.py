#!/usr/bin/env python3
"""auth module"""

from flask import request
from api.v1.views import app_views
from models.user import User
from typing import List, Type
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header"""
        if (authorization_header is None or
                type(authorization_header) is not str
                or authorization_header[:6] != 'Basic '):
            return None
        return authorization_header[6:]
