#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Tuple, TypeVar, Optional


class BasicAuth(Auth):
    """ Basic Authentication Class """

    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """ Extracts Base64 encoded part from the Authorization header. """
        if authorization_header and isinstance(authorization_header, str) and authorization_header.startswith("Basic "):
            return authorization_header.split(" ", 1)[1]
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """ Decodes a Base64 encoded string. """
        if base64_authorization_header and isinstance(base64_authorization_header, str):
            try:
                decoded_bytes = b64decode(base64_authorization_header)
                return decoded_bytes.decode("utf-8")
            except (TypeError, ValueError, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts user email and password from a decoded Base64 string.
        Returns a tuple (email, password).
        """
        if decoded_base64_authorization_header and isinstance(decoded_base64_authorization_header, str):
            if ":" in decoded_base64_authorization_header:
                return tuple(decoded_base64_authorization_header.split(":", 1))
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """
        Returns the User instance if the credentials are valid, None otherwise.
        """
        if not user_email or not user_pwd or not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            found_users = User.search({'email': user_email})
            for user in found_users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """ Retrieves the User instance for a request based on Authorization header. """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        encoded = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(encoded) if encoded else None

        if decoded:
            email, pwd = self.extract_user_credentials(decoded)
            if email and pwd:
                return self.user_object_from_credentials(email, pwd)
        return None

