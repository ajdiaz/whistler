#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from twitter import Twitter, OAuth
from whistler.bot import restricted, EVENT_CHANGE_STATUS

def post(message, token, token_key, con_secret, con_secret_key):
      t = Twitter(
              auth = OAuth(token, token_key, con_secret, con_secret_key)
      )
      t.statuses.update(
              status=message
      )

class PostMixin(object):
    """Bot mix-in which post a tweet into twitter account
    """

    def __init__(self, token, token_key, con_secret, con_secret_key):
        self.token = token
        self.token_key = token_key
        self.con_secret_key = con_secret_key
        self.con_secret = con_secret

    @restricted
    def cmd_post(self, msg, args):
        "Post a message to twitter"
        if len(args):
            post(" ".join(args), self.token, self.token_key,
                    self.con_secret, self.con_secret_key)
            return "post: %s" % " ".join(args)


