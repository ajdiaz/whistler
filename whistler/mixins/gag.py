#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from addons.htmlparse import htmlparse


class GagMixin(object):
    """Return a random image from 9gag"""

    def cmd_gag(self, msg, args):
        """!gag   - return a random image from 9gag."""

        try:
            data = htmlparse("http://9gag.com/random", ".badge-item-animated-img")
            title = data.attr("alt")
            img = data.attr("src")
        except:
            data = htmlparse("http://9gag.com/random", ".badge-item-img")
            title = data.attr("alt")
            img = data.attr("src")
            # We need to duplicate data access here cuz of the object is not really parsed until
            # attr is invoked.

        self.send(msg['from'], img, msg['type'])

        return str(title)


