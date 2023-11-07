#!/usr/bin/env python3
"""
Authentication through class
"""
from flask import request
from typing import List
from typing import TypeVar

class Auth:
    """auth class"""


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false
        """
        return False


    def authorization_header(self, request=None) -> str:
        """returns None
        """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None
        """
        return None
