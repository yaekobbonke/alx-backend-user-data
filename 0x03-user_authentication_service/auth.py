#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid
from typing import Optional


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
        """register user
        """
        if email and password:
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                user = self._db.add_user(email, _hash_password(password))
                return user
            else:
                raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ validate login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """ Generate UUIDs
        """
        my_id = str(uuid.uuid4())
        return my_id

    def create_session(self, email: str) -> str:
        """Get session ID
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Find user by session ID
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """Destroy session
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token
        """
        try:
            user = self._db.find_user_by(email)
            if user:
                token = _generate_uuid()
                self._db.add_user(token)
                return jsonify({'email': email, 'token': token})
            else:
                abort(401)
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password
        """
        try:
            user = self._db.find_user_by(reset_token)
            if user:
                new_password = bcryp.hashpw(password.encode('utf-8'),
                                            gensalt())
                update_user(new_password, reset_token=None)
            else:
                abort(403)
        except ValueError:
            abort(403)
