#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import wolframalpha


class QuestionMixin(object):
    """Return the answer of everything"""

    def __init__(self, appid):
        self.appid = appid

    def cmd_question(self, msg, args):
        """!question <text>  - ask for the meaning of life and everything."""

        client = wolframalpha.Client(self.appid)
        res = client.query(" ".join(args))

        ret=''
        for pod in res.pods:
            if ret:
                self.send(msg['from'], ret, msg['type'])
                ret = ''
            if pod.text:
                ret = "'''"
                ret += str(pod.title)
                ret += "\n"
                ret += "=" * len(str(pod.title))
                ret += "\n"
                ret += str(pod.text)
                ret += "\n'''"

        return ret

