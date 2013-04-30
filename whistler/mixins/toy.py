#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""
The Toy mixin provide you a suite of toys to play with the bot. Nothing
serious happens here.
"""

from whistler.bot import restricted
from whistler.mixins import command_output


class ToyMixin(object):
    def cmd_wtf(self, msg, args):
        """Uses the "wtf" tool to define acronyms and words."""
        args.insert(0, "/usr/games/wtf")
        return command_output(args)

    def cmd_uptime(self, msg, args):
        """Obtain the uptime of the machine running the bot."""
        return command_output(("/usr/bin/uptime"))

    def cmd_whoami(self, msg, args):
        """Who are you?"""
        return "you are %s" % msg["from"]

    def cmd_rooms(self, msg, args):
        """List joined rooms"""
        return "rooms: " + ", ".join(self.rooms)

    def cmd_users(self, msg, args):
        """List admin users"""
        return "users: " + ", ".join(self.users)

    @restricted
    def cmd_stop(self, msg, args):
        """Exits the bot"""
        self.reply(msg, "Bye Bye!")
        self.stop()



