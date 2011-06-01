#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:
#
# Copyright © 2010 Adrian Perez <aperez@igalia.com>

"""
Poll mixing to create MUC based polls.
"""

class Poll(object):
    """Represents a poll with several choices."""

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
        """Adds a choice to the poll."""
        self.choices.append(choice)
        self.votecount.append(0)


class PollMixin(object):
    """Implements a simple polls system as a mix-in for :class:`WhistlerBot`."""

    def __init__(self, *args, **kw):
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
                poll.vote(msg["from"].bare, choice)
                return "Your vote has been recorded, thanks"
            except ValueError, e:
                return str(e)

        else:
            return "Wrong number of arguments (%i)" % len(args)


