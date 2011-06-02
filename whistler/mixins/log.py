#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""
A Log Mixin which providing basic log features to Whistler Bot
"""

from whistler.bot import EVENT_MESSAGE
from whistler.log import WhistlerLog

class LogMixin(object):
    """Implements a basic log features for a :class:`WhistlerBot`."""

    def __init__(self, *args, **kw):
        """Create a new log mixin."""

        if not getattr(self, "log", None):
            self.log = WhistlerLog()

        self.register_handler(EVENT_MESSAGE, self.save_log_message)

    def save_log_message(self, message, args):
        self.log.info("[%s] <%s> %s" % (
            "room" if message["type"] == "groupchat" else "chat",
            message["from"],
            message["body"],
         ))

