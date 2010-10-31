#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""
The log module
--------------

The log module provide a transparent way to handle log messages from
whistler, no any other secret here.
"""

import logging

LOG_INFO = logging.INFO
LOG_DEBUG = logging.DEBUG
LOG_ERROR = logging.ERROR
LOG_WARNING = logging.WARNING
LOG_CRITICAL = logging.CRITICAL

class WhistlerLog(logging.getLoggerClass()):

    message_format  = "[%(asctime)s] %(levelname)s: %(message)s"
    datetime_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, level=logging.INFO):
        logging.getLoggerClass().__init__(self, None)
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter(self.message_format,
                self.datetime_format)
        self.handler.setFormatter(self.formatter)
        self.addHandler(self.handler)
        self.setLevel(level)


