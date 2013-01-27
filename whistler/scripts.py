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

import logging
import sys, os, io

try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser

from whistler.bot import WhistlerBot
from whistler.mixins import BotFactory


DEFAULT_CONFIG = {
    "server":   "speeqe.com",
    "account":  "speeqe.com",
    "resource": "whistler",
    "password": "doesnotmatter",
    "port":      5222,
    "use_tls":   False,
    "ignore_ssl_cert": True,
    "loglevel":  logging.WARNING
}

def get_no_defaults(config, section):
    defaults = set(config.defaults().items())
    sectvals = set(config.items(section))
    return list(sectvals - defaults)

def main():
    """Main console script function.

    Runs an operational bot on a specific room list which is defined in
    the command line.

    """
    config  = RawConfigParser(DEFAULT_CONFIG)

    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        print >> sys.stderr, "usage: whistler <config>"
        return 1

    try:
        config.read(sys.argv[1])
    except:
        print >> sys.stderr, "unable to read config file %s." % sys.argv[1]
        return 1

    mixins = map(lambda x:x[6:], filter(lambda x:x[0:6] == "mixin:", config.sections()))
    rooms  = map(lambda x:x[5:], filter(lambda x:x[0:5] == "room:",  config.sections()))

    factory = BotFactory(dict([(x, dict(get_no_defaults(config,"mixin:%s" % x))) for x in mixins]))

    logging.basicConfig(
            level=config.getint("DEFAULT", "loglevel"),
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
    )

    Bot = factory(mixins)
    bot = Bot(
              jid      = config.get("DEFAULT", "account"),
              password = config.get("DEFAULT", "password"),
              resource = config.get("DEFAULT", "resource"),
              use_tls  = config.get("DEFAULT", "use_tls"),
              server   = ( config.get("DEFAULT", "server"),
                           config.getint("DEFAULT", "port") ),
              rooms    = rooms,
              ignore_ssl_cert = config.get("DEFAULT", "ignore_ssl_cert")
    )

    try:
        bot.start()
    except KeyboardInterrupt:
        bot.stop()


