#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


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
        ''' def register user '''
        if email and password:
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                user = self._db.add_user(email, _hash_password(password))
                return user
            else:
                raise ValueError("User {} already exists".format(email))
