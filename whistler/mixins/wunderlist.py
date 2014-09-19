#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from wunderpy import Wunderlist
from wunderpy import api

class WunderlistMixin(object):
    """Bot mixin to use wunderlist to add todo list
    """

    def __init__(self, wunder_user, wunder_password, wunder_list='inbox', **kwargs):
        self.wunder_user = wunder_user
        self.wunder_password = wunder_password
        self.wunder_list = wunder_list

    def cmd_wunderlist(self, msg, args):
        """add/delete/list tasks in wunderlist

        !wunderlist <list|add|del> [taskid/message] - manage tasks in wunderlist
        """

        def _wlogin():
            w = Wunderlist()
            w.login(self.wunder_user, self.wunder_password)
            w.update_lists()
            return w

        if len(args) < 1:
            return "Missing arguments"

        cmd = args[0]

        if cmd == "list":
            w = _wlogin()
            ret = []
            for task in w.tasks_for_list(self.wunder_list):
                if not task.completed:
                    ret.append("[`%s`] *%s*" % (task.id, task.title,))

            if ret:
                return "\n".join(ret)
            else:
                return "No tasks :thumbsup:"
        elif cmd == "add":
            if len(args)<2:
                return "Missing arguments"
            txt = " ".join(args[1:])
            w = _wlogin()
            w.add_task(txt, list_title=self.wunder_list,)
            return "Task added"
        elif cmd == "del":
            if len(args)<2:
                return "Missing arguments"
            tid = args[1]
            w = _wlogin()
            try:
                w.send_request(api.calls.delete_task(tid))
                return "Done"
            except BaseException as e:
                return "Error when deleting: %s" % (str(e),)
        elif cmd == "done":
            if len(args)<2:
                return "Missing arguments"
            tid = args[1]
            w = _wlogin()
            try:
                w.send_request(api.calls.complete_task(tid))
                return "Task done! :thumbsup:"
            except BaseException as e:
                return "Error when closing: %s" % (str(e),)
        else:
            return "Unknown command"




