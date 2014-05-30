#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""
Useful mix-in classes to add prebuilt behavior to custom bots.
"""

import os
import imp
import sys
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
    WhistlerBot.__init__(self, *args, **kw)

    for mixin in self.mixins:
        if mixin._factory_name in self._factory_options:
            mixin.__init__(self, **self._factory_options[mixin._factory_name])
        else:
            mixin.__init__(self)


class BotFactory(object):
    """Create a new bot class using mixins passed in call."""

    def __init__(self, options={}):
        """Create a new factory.
        :param `options`: a :class:`dict` indexed by mixin name which
            contains a list of options to be passed as argument at init
            process of the mixin.

        """
        self.options = options

    def bot_class_import(self, name):
        base = "whistler.mixins."

        modname = base + name
        klsname = name.capitalize() + "Mixin"

        try:
            mod = __import__(modname, globals(), locals(), [klsname])
            kls = getattr(mod, klsname)
            kls._factory_name = name
        except ImportError:
            mod = imp.load_source("whistler.mixin." + name, os.path.join(os.getcwd(), name + ".py"))
            kls = getattr(mod, klsname)

        return kls

    def __call__(self, mixins=[]):
        args = [WhistlerBot]
        mixs = map(self.bot_class_import, mixins)
        args.extend(mixs)

        return type("NewBot", tuple(args), {
            "mixins": mixs,
            "_factory_options": self.options,
            "__init__": _bot_init
        })


