#!/usr/bin/env python3
""" Personal Data Module"""
import logging
import re


def filter_datum(fields, redaction, message, separator):
    pattern = fr"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, fr"\1={redaction}", message)
