#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2010 Adrian Perez <aperez@igalia.com>
# Copyright © 2010 Andrés J. Díaz <ajdiaz@connectical.com>

"""
Useful mix-in classes to add prebuilt behavior to custom bots.
"""

import inspect
import threading
from whistler.bot import restricted

class HelpCommandMixin(object):
    """
    Mix-in class which adds a "help" command to a :class:`WhistlerBot`. To
    use it in your custom bot, do something like:

    >>> class MyBot(WhistlerBot, HelpCommandMixin):
    ...     pass

    """
    def __get_commands(self):
        for (name, kind, _, _) in inspect.classify_class_attrs(self.__class__):
            if name.startswith("cmd_") and kind == "method":
                yield name[4:]

    def cmd_help(self, cmd, args):
        """Obtains a list of commands, or help about a particular command."""
        if not args:
            return "Available commands: " + ", ".join(self.__get_commands())

        func = getattr(self, "cmd_" + args[0], None)
        if func is None:
            return "No such command '%s'" % args[0]

        return "%s: %s" % (args[0], inspect.getdoc(func))


class PatchQueueMixin(object):
    """
    Mix-in class with add a number of patchbot commands, more of them is
    based on #exherbo IRC patchbot, which is explained in
    http://2tu.us/2sjr, you can use this mixin as followin explained:

    >>> class MyBot(WhistlerBot, PatchQueueMixin):
    ...     pass
    """

    cache = {}
    index = 0
    lock = threading.RLock()

    def cmd_patchdone(self, cmd, args):
        """ Remove a patch from the patchlist. Example: !pd 445 """

        for patch in args:
            try:
                self.cache.pop(int(patch))
            except KeyError:
                return "patch #%d is not in queue"


    def cmd_patchlist(self, cmd, args):
        """ Show the patch in current queue. Example: !pl [project]+ """
        ret = ""

        for patch in self.cache.keys():
            if len(args):
                if self.cache[patch]["project"] in args:
                    ret += "#%(id)d: %(url)s [%(project)s] %(desc)s\n" % self.cache[patch]
            else:
                ret += "#%(id)d: %(url)s [%(project)s] %(desc)s\n" % self.cache[patch]

        return ret


    def cmd_patchqueue(self, cmd, args):
        """
        Enqueue a patch into the queue.
        Example: !pq <url> <project> [desc]
        """

        if len(args) < 2:
            return "A valid patch URL and project is mandatory!"

        if len(args) > 2:
            desc = " ".join(args[2:])
        else:
            desc = ""

        with self.lock:
            patchid = self.index
            self.index +=1

        self.cache[patchid] = {
                'id': patchid,
                'url': args[0],
                'project': args[1],
                'desc': desc
        }

        return "Enqueued #%d" % patchid

    cmd_pq = cmd_patchqueue
    cmd_pl = cmd_patchlist
    cmd_pd = cmd_patchdone

