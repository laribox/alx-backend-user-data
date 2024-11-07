#!/usr/bin/env python3
"""
This module provides functionality to obfuscate sensitive information in log messages.
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in the log message.

    Args:
        fields (List[str]): The list of field names to obfuscate.
        redaction (str): The string to replace field values with.
        message (str): The original log message to obfuscate.
        separator (str): The character that separates each field in the message.

    Returns:
        str: The obfuscated log message.
    """
    # Create a regex pattern to match each field and replace its value with the redaction
    for field in fields:
        message = re.sub(f"{field}=[^;]*", f"{field}={redaction}", message)
    return message

