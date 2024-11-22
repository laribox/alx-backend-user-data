#!/usr/bin/env python3
"""
Auth module for user authentication.
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""
    def __init__(self):
        self._db = DB()

    @staticmethod
    def _generate_uuid() -> str:
        """Generate a new UUID."""
        return str(uuid.uuid4())

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user's login credentials."""
        user = self._db.find_user_by(email=email)
        if user and bcrypt.checkpw(password.encode('utf-8'),
                                   user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """Create a new session for a user."""
        user = self._db.find_user_by(email=email)
        if not user:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
