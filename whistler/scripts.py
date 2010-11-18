#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:
#
# Copyright (C) 2010 Andres J. Diaz <ajdiaz@connectical.com>
# Copyright (C) 2010 Adrian Perez <aperez@igalia.com>


"""
The scripts module
------------------

The scripts module provide and endpoint for console scripts, like whistler
command, provided in basic whistler package.

"""

import sys
import subprocess
from optparse import OptionParser

from whistler.bot import WhistlerBot, restricted
from whistler.mixins import HelpCommandMixin, PollsMixin


def command_output(cmd):
    cmd = subprocess.Popen(cmd,
            stdin  = None,
            stderr = subprocess.PIPE,
            stdout = subprocess.PIPE)
    out, err = cmd.communicate()
    cmd.wait()
    if cmd.returncode == 0:
        return out
    else:
        return "Error (%i): %s" % (cmd.returncode, err)


class FooBot(WhistlerBot, HelpCommandMixin, PollsMixin):
    def __init__(self, *arg, **kw):
        WhistlerBot.__init__(self, *arg, **kw)
        HelpCommandMixin.__init__(self)
        PollsMixin.__init__(self)

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

    def cmd_lsrooms(self, msg, args):
        """List joined rooms"""
        return "rooms: " + ", ".join(self.client["xep_0045"].rooms.keys())

    def cmd_lsusers(self, msg, args):
        """List admin users"""
        return "users: " + ", ".join(self.users)

    @restricted
    def cmd_stop(self, msg, args):
        """Exits the bot"""
        self.stop()


def main():
    """Main console script function.

    Runs an operational bot on a specific room list which is defined in
    the command line.

    """
    parser = OptionParser()
    parser.add_option("-r", "--resource", action="store", dest="resource",
        default="whistler", type="str", help="The bot resource name.")

    parser.add_option("-s", "--server", action="store", dest="server",
       default=None, type="str", help="Server to connect to.")

    parser.add_option("-p", "--port", action="store", dest="port", type="int",
       default=5222, help="Specify a different destination port.")

    parser.add_option("-P", "--password", action="store", dest="password",
        type="str", default="", help="Specify user password.")

    parser.add_option("-D", "--debug", action="store_true", dest="debug",
        default=False, help="Run in debug mode.")

    parser.add_option("-R", "--room", action="append", dest="rooms",
        default=[], help="Join into this room (option can be repeated.")

    parser.add_option("-U", "--user", action="append", dest="users",
        default=[], help="Set the user as master user (option can be repeated.")

    # Parse options
    options, args = parser.parse_args()

    if len(args) < 1:
        raise IndexError("usage: %s [options] <JID>" % sys.argv[0])

    if options.server:
        options.server = ( options.server, options.port )

    options.jid = args[0]

    bot = FooBot(options.jid, options.password,
                 server=options.server,
                 resource=options.resource,
                 rooms=options.rooms,
                 users=options.users)

    try:
        bot.start()

    except KeyboardInterrupt:
        pass

    finally:
        bot.stop()


