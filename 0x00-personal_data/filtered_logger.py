#!/usr/bin/env python3
""" Personal Data Module"""
import logging
import re
from typing import Tuple


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
        message = record.getMessage()
        redacted_message = filter_datum(
             self.fields,
             self.REDACTION,
             message,
             self.SEPARATOR
            )
        record.msg = redacted_message
        return super().format(record)
