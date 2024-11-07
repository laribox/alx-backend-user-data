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
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for
    handling user data with PII obfuscation.

    Returns:
        logging.Logger: A configured logger with RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    connect to mysql database
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    try:
        connector = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pwd,
            database=db_name,
        )
    except mysql.connector.Error:
        return None

    return connector


def main() -> None:
    """
    function will obtain a database connection using get_db and retrieve
    all rows in the users table and display each row under a filtered format
    """
    db = get_db()
    if not db:
        return

    logger = get_logger()
    cursor = db.cursor()
    columns = "name,email,phone,ssn,password,ip,last_login,user_agent"
    cursor.execute("SELECT {} FROM users".format(columns))
    rows = cursor.fetchall()
    fmt = "name={}; email={}; phone={}; ssn={}; password={}; ip={};" + \
        " last_login={}; user_agent={};"

    for row in rows:
        formatted_row = fmt.format(
            row[0], row[1], row[2], row[3], row[4],
            row[5], row[6], row[7]
        )
        logger.info(formatted_row)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
