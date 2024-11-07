#!/usr/bin/env python3
"""
This module provides a function for hashing passwords with bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a salt using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if a password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain text password to verify.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
