#!/usr/bin/env python3
""" Personal Data Module"""
import logging
import re
from typing import Tuple

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields, redaction, message, separator):
    pattern = fr"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, fr"\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
             self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger
