#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from user import *
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash password"""
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return_byte = bcrypt.hashpw(password, salt)

    return return_byte


class Auth:
    """Auth class to interact with \
            the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """take mandatory email and password \
                arguments and return a User object
        """

        if email and password:
            raise ValueError(f"User {email} already exists")
        else:
            hashed_password = _hash_password(password)

            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
        return user
