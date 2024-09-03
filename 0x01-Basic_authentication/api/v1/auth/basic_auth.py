#!/usr/bin/env python3
"""auth module"""

from flask import request
from api.v1.views import app_views
from models.user import User
from typing import List, Type
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Auth class"""
