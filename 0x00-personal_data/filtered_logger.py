#!/usr/bin/env python3
"""
This module provides functionality to
obfuscate sensitive information in log messages.
"""

import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates specified fields in the log message.
    """
    pattern, repl = regex["pattern"], regex["repl"]
    return re.sub(pattern(fields, separator), repl(redaction), message)
