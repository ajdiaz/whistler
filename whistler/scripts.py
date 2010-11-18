#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:


"""
The scripts module
------------------

The scripts module provide and endpoint for console scripts, like whistler
command, provided in basic whistler package.

"""

import sys
from optparse import OptionParser
from whistler.bot import WhistlerBot, restricted, EVENT_REGISTER
from whistler.log import WhistlerLog
from whistler.mixins import PatchQueueMixin


class MainWhistlerBot(WhistlerBot, PatchQueueMixin):
    """Extend basic whistler bot, adding some functionalities."""

    def on_register_user(self, who):
        self.send_to(who,"Hi %s, now you are a whistler administrator." % who)


    def cmd_ping(self, msg, args):
        return "pong"


    def cmd_whistler(self, msg, args):
        return "/me is an XMPP bot with MUC (multi-user-conference) " + \
               "support easy to extend, written in Python using xmppy module."


    @restricted
    def cmd_join(self, msg, args):
        self.join(args)


    @restricted
    def cmd_leave(self, msg, args):
        self.leave(args)


    @restricted
    def cmd_quit(self, msg, args):
        self.stop()


    @restricted
    def cmd_user(self, msg, args):
        if not args:
            return "\n".join(self.users)

        if len(args) >= 2:
            if args[0].lower() == "add":
                for user in args[1:]:
                    self.register_user(user)
            elif args[0].lower() == "del":
                for user in args[1:]:
                    self.unregister_user(user)


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

    log = WhistlerLog()

    try:
        if len(args) < 1:
            raise IndexError("usage: %s [options] <JID>"
                    % sys.argv[0])

        if options.server:
            options.server = ( options.server, options.port )

        options.jid   = args[0]

        log.info("starting bot...")

        bot = MainWhistlerBot( jid = options.jid, password = options.password,
                rooms = options.rooms, server = options.server, log = log,
                resource = options.resource, users = set(options.users))
        bot.debug = options.debug
        bot.register_handler(EVENT_REGISTER, bot.on_register_user)

        try:
            bot.start()

        except KeyboardInterrupt:
            pass

        finally:
            bot.stop()

    except Exception, e:
        if options.debug:
            raise
        else:
            log.critical("unexpected error: %s" % e)
        sys.exit(1)

