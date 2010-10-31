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
from whistler.bot import WhistlerBot
from whistler.log import WhistlerLog

class MainWhistlerBot(WhistlerBot):
    """ Extend basic whistler bot, adding some functionalities. """

    def cmd_ping(self, msg, args):
        return "pong"

def main():
    """ Main console script function, which run a operational bot on an
    specific room list which is defined in command line. """

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
            default=False, help="run in debug mode.")

    # Parse options
    options, args = parser.parse_args()

    log = WhistlerLog()

    try:
        if len(args) < 2:
            raise IndexError("usage: %s [options] <JID> [room]+"
                    % sys.argv[0])

        if options.server:
            options.server = ( options.server, options.port )

        options.jid   = args[0]
        options.rooms = args[1:]

        log.info("starting bot...")

        bot = MainWhistlerBot( jid = options.jid, password = options.password,
                rooms = options.rooms, server = options.server, log = log,
                resource = options.resource )

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

