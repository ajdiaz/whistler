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


class Poll(object):
    """
    Represents a poll with several choices.
    """
    def __init__(self, description=None):
        self.description = description
        self.voteuids    = set()
        self.votecount   = []
        self.choices     = []

    def vote(self, uid, option):
        """Votes for a given choice.

        :param uid: Unique identifier for the person emitting this vote.
            This is used to check that the same does not vote more than
            once.
        :param option: Index (1-based) of the option chosen.
        """
        if uid in self.voteuids:
            raise ValueError("User already voted")

        self.voteuids.add(uid)

        try:
            self.votecount[option-1] += 1
        except IndexError:
            raise ValueError("Option %r is not valid" % option)

    def add(self, choice):
        """Adds a choice to the poll.
        """
        self.choices.append(choice)
        self.votecount.append(0)


class PollsMixin(object):
    """Implements a simple polls system as a mix-in for :class:`WhistlerBot`.
    """
    def __init__(self):
        self._polls = {}

    def cmd_poll(self, msg, args):
        """Create polls and manage them. Usage:

            !poll              - Show list of polls
            !poll <id>         - Show poll
            !poll <id> new <d> - Create a new poll with the given description
            !poll <id> del     - Delete a poll
            !poll <id> add <c> - Add a choice to a poll
        """
        if not len(args):
            return "Polls: " + ", ".join(self._polls.iterkeys())

        if args[0] not in self._polls:
            if len(args) > 2 and args[1] in ("new", "description"):
                self._polls[args[0]] = Poll(" ".join(args[2:]))
                return "Poll \"%s\" created" % args[0]
            else:
                return "No such poll \"%s\"" % args[0]

        poll = self._polls[args[0]]

        if len(args) == 1:
            result = "Poll: %s\nResults:" % poll.description
            for i in xrange(len(poll.choices)):
                result += "\n  %i.) %s -- %i" % (i+1,
                        poll.choices[i], poll.votecount[i])
            return result

        if len(args) == 2 and args[1] == "del":
            del self._polls[args[0]]
            return "Poll \"%s\" deleted" % args[0]

        if len(args) > 2 and args[1] == "add":
            text = " ".join(args[2:])
            poll.add(text)
            return "Choice \"%s\" added" % text

        if len(args) > 2 and args[1] in ("new", "description"):
            return "Poll \"%s\" already exists" % args[0]

        return "Bad poll command syntax?"


    def cmd_vote(self, msg, args, jid=None):
        """Vote in a poll. Can receive one or two arguments:

            !vote            - Show list of active polls
            !vote <id>       - Show available options in a poll
            !vote <id> <opt> - Vote for a given choice in a poll
        """
        if not len(args):
            return "Active polls: " + ", ".join(self._polls.iterkeys())

        if len(args) == 1:
            if args[0] not in self._polls:
                return "No such poll \"%s\"" % args[0]

            poll = self._polls[args[0]]
            result = "Poll: %s\nChoices:" % poll.description
            for i in xrange(len(poll.choices)):
                result += "\n  %i.) %s" % (i+1, poll.choices[i])
            return result

        elif len(args) == 2:
            if args[0] not in self._polls:
                return "No such poll %r" % args[0]

            poll = self._polls[args[0]]

            try:
                choice = int(args[1])
            except ValueError:
                return "Choice %r is not an integer" % args[1]

            try:
                if not msg.getFrom().getResource():
                    return ("Error: voting cannote be recorded if user's"
                            " resource is not available")
                poll.vote(str(msg.getFrom()), choice)
            except ValueError, e:
                return e

        else:
            return "Wrong number of arguments (%i)" % len(args)


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

