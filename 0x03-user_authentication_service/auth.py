#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return_byte = bcrypt.hashpw(password, salt)
    return return_byte
