#!/usr/bin/env python3
""" Personal Data Module"""
import logging
import re
from typing import Tuple
import mysql.connector
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, rf"\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str]):
        """ Redacting Formatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format function"""
        record.msg = filter_datum(
             self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ Get Logger function"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db():
    """ Get DB function"""
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    database = os.getenv('PERSONAL_DATA_DB_NAME', '')

    connection = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=database
    )
    return connection


def main():
    """main function"""
    db = get_db()
    logger = get_logger()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            for row in cursor:
                message = "; ".join(
                    [f"{key}={value}" for key,
                     value in zip(cursor.column_names, row)]) + ";"
                logger.info(message)
    finally:
        db.close()


if __name__ == "__main__":
    main()
