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
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if path is None or excluded_paths is None:
            return True
        path = path + '/' if path[-1] != '/' else path
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None
        """
        return None
