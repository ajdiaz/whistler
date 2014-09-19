#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import htmldom

def htmlparse(url, selector=None):
    dom = htmldom.HtmlDom(url).createDom()
    if selector is not None:
        items = dom.find(selector)
    else:
        items = dom
    return items


class HtmlparseMixin(object):
    """Bot mix-in which parse a URL and return the content of specified element into the DOM"""

    def cmd_htmlparse(self, msg, args):
        """!htmlparse <url> [selector]   - parse the specified url and return the selector content."""

        if len(args) == 0:
            return "Missing arguments"

        try:
            return str(htmlparse(args[0], " ".join(args[1:])).html())
        except Exception as e:
            return "Something wrong happened here :(\n" + str(e)


