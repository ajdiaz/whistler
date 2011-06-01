#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""
Useful mix-in classes to add prebuilt behavior to custom bots.
"""

import subprocess
from whistler.bot import WhistlerBot


def command_output(cmd):
    """Utility which returns the output of a system command."""
    cmd = subprocess.Popen(cmd,
            stdin  = None,
            stderr = subprocess.PIPE,
            stdout = subprocess.PIPE)
    out, err = cmd.communicate()
    cmd.wait()
    if cmd.returncode == 0:
        if out[-1] == "\n":
            return out[:-1] # remove last \n
        else:
            return out
    else:
        return "Error (%i): %s" % (cmd.returncode, err)


def _bot_init(self, *args, **kw):
    for mixin in self.mixins:
        mixin.__init__(self, *args, **kw)


class BotFactory(object):
    """Create a new bot class using mixins passed in call."""
    def bot_class_import(self, name):
        base = "whistler.mixins."

        modname = base + name
        klsname = name.capitalize() + "Mixin"

        mod = __import__(modname, globals(), locals(), [klsname])
        return getattr(mod, klsname)

    def __call__(self, mixins=[]):
        args = [WhistlerBot]
        args.extend(map(self.bot_class_import, mixins))

        return type("NewBot", tuple(args), { "mixins":args, "__init__": _bot_init })


