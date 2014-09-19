#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os


class NoteMixin(object):
    """Save and read notes"""

    def __init__(self, path, **kwargs):
        self.path = path

    def cmd_note(self, msg, args):
        """!note <get|set|del> <notename> [text] - manipulate notes"""

        if len(args)<2:
            return "Missing arguments"

        cmd = args[0]
        dat = args[1]


        if "." in dat:
            return "dots are not allowed in notename"

        if cmd == "set":
            if len(args)<3:
                return "set command needs more arguments"
            txt = " ".join(args[2:])
            try:
                with file(os.path.join(self.path, "%s.txt" % (dat,)), 'w') as f:
                    f.write(txt)
                return "note set!"
            except BaseException as e:
                return "unable to set the note: %s" % (e,)
        elif cmd == "get":
            try:
                with file(os.path.join(self.path, "%s.txt" % (dat,)), 'r') as f:
                    return "\n".join(f.readlines())
            except BaseException as e:
                return "No note with this name found: %s" % (e,)
        elif cmd == "del":
            try:
                os.remove(os.path.join(self.path, "%s.txt" % (dat,)))
                return "note removed!"
            except BaseException as e:
                return "unable to remove note" % (e,)
        elif cmd == "add":
            if len(args)<3:
                return "add command needs more arguments"
            txt = " ".join(args[2:])
            try:
                f = file(os.path.join(self.path, "%s.txt" % (dat,)), 'r')
                l = f.readlines()
                f.close()
                l.append(txt)
                f = file(os.path.join(self.path, "%s.txt" % (dat,)), 'w')
                f.write("\n".join(l))
                f.close()
                return "note set!"
            except BaseException as e:
                return "unable to add text in note: %s" % (e,)
        else:
            return "Invalid command"

