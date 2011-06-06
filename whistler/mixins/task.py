#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from whistler.bot import restricted, EVENT_CHANGE_STATUS
from datetime import datetime

class Task(object):
    def __init__(self, ident, author, message):
        self.ident   = ident
        self.author  = author
        self.message = message
        self.created = datetime.now()

    def __str__(self):
        return "#%d %s (%s at %s)" % (
                self.ident,
                self.message,
                self.author,
                self.created.isoformat(' ')
        )

class TaskMixin(object):
    """Bot mix-in which adds task command to send tasks to users. """

    def __init__(self):
        self.tasks = {}
        self.register_handler(EVENT_CHANGE_STATUS, self.task_userlogin)

    def task_userlogin(self, presence):
        """Handle task output when a user login."""
        user = presence.get_from().bare
        if user == self.jid:
            return

        if presence.get_type() != "available":
            return

        if user in self.tasks:
            self.send(user, self.show_tasks(user))

    def show_tasks(self, who):
        """Return an string with the list of tasks"""
        if who in self.tasks and len(self.tasks[who]):
            ret = "Hi, %s. These are your tasks:\n" % who
            for x in self.tasks[who]:
                ret += str(self.tasks[who][x]) + "\n"
            return ret
        else:
            return "Congrats %s, you do not have waiting tasks." % who

    @restricted
    def cmd_task(self, msg, args):
        """Manage tasks for users.

        task [list|show]
        task <new|open|add|create> <user> <task text>
        task <close|del|delete|remove> <task id>
        """
        user = msg["from"].bare

        if len(args) == 0 or args[0] == "list" or args[0] == "show":
            return self.show_tasks(user)

        if args[0] == "new"  or args[0] == "create" or \
           args[0] == "open" or args[0] == "add":
               if len(args) < 3:
                   return "not enough arguments, required \"to whom\" and \"what\""
               if args[1] in self.tasks:
                   task = Task(
                       len(self.tasks[args[1]]),
                       user,
                       " ".join(args[2:])
                   )
                   self.tasks[args[1]][task.ident] = task
               else:
                   task = Task(0, user," ".join(args[2:]))
                   self.tasks[args[1]] = {
                           task.ident: task
                   }

               return str(task)

        if args[0] == "close" or args[0] == "del" or \
           args[0] == "delete" or args[0] == "remove":
               if len(args) < 2:
                   return "not enough arguments, required \"id\""
               try:
                   ident = int(args[1])
               except ValueError:
                   return "Id field must be a number"

               if user not in self.tasks:
                   return "You do not have any task to close."

               if ident not in self.tasks[user]:
                   return "Sorry this id do not exists"

               del self.tasks[user][ident]

               return "#%d closed" % ident


