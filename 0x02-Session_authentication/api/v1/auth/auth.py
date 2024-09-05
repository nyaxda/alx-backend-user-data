#!/usr/bin/env python3
"""auth module"""

from flask import request
from api.v1.views import app_views
from models.user import User
from typing import List, Type
import re
from os import getenv


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth"""
        # if path is None or excluded_paths is
        # None or len(excluded_paths) == 0:
        #     return True
        # if path[-1] != '/':
        #     path += '/'
        # if path in excluded_paths:
        #     return False
        # return True
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> Type[User]:
        """current_user"""
        return None

    def session_cookie(self, request=None):
        if request is None:
            return None
        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
