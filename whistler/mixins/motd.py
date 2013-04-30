#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from whistler.bot import restricted, EVENT_CHANGE_STATUS
from datetime import datetime

class MotdMixin(object):
    """Bot mix-in which send a message when a user login.
    """

    def __init__(self, message=None):
        self.register_handler(EVENT_CHANGE_STATUS, self.task_userlogin)
        self.message = message

    def task_userlogin(self, presence):
        """Handle message output when a user login.
        """
        user = presence.get_from().bare
        if user == self.user:
            return

        if user in self.rooms:
            return

        if presence.get_type() != "available":
            return

        if self.message:
            self.send(presence.get_from(), self.message )

    @restricted
    def cmd_motd(self, msg, args):
        "Set the Message-of-the-day"
        if len(args):
            self.message = " ".join(args)
        else:
            self.message = None
        return "MOTD setted to: %s" % self.message



