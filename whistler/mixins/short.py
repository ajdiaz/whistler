#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""A Short Mixin which providing basic URL shorting service using bit.ly
"""

import bitly_api

from whistler.bot import EVENT_MESSAGE
from whistler.log import WhistlerLog

def short(x, api_user, api_key):
    b = bitly_api.Connection(api_user, api_key)
    return b.shorten(x)["url"]


class ShortMixin(object):
    """Implements a basic URL shorting services using bit.ly
    """

    def __init__(self, api_user, api_key):
        """Create a new short mixin.
        """
        self.api_user = api_user
        self.api_key = api_key

    def cmd_short(self, msg, args):
        "URL shortening service using bit.ly, just type short <url>+"
        return "\n".join(map(lambda x:short(x, self.api_user, self.api_key), args))

