#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from addons.htmlparse import htmlparse


class DevopsmeMixin(object):
    """Return a random image from devopsreactions"""

    def cmd_devopsme(self, msg, args):
        """!devopsme   - return a random image from devopsreactions."""

        data = htmlparse("http://devopsreactions.tumblr.com/random", ".item_content")

        title = data.find(".post_title").find("a").text()
        img = data.find("p").find("img").attr("src")

        self.send(msg['from'], img, msg['type'])

        return str(title)


