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

regex = {
    "pattern": lambda f, s: r"(?P<field>{})=[^{}]+".format("|".join(f), s),
    "repl": lambda r: r"\g<field>={}".format(r),
}


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates specified fields in the log message.
    """
    pattern, repl = regex["pattern"], regex["repl"]
    return re.sub(pattern(fields, separator), repl(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum """

        if not isinstance(record, logging.LogRecord):
            raise TypeError("record must be an instance of logging.LogRecord")
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
