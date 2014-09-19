#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from buffpy import *
from buffpy.managers.profiles import Profiles


class BufferMixin(object):
    """Bot mix-in which post to social networks using bufferapp.com
    """

    def __init__(self, apitoken, cis, cid, **kwargs):
        self.apitoken = apitoken
        self.cis = cis
        self.cid = cid
        self.profiles = kwargs
        self.data = None

    def cmd_buffer(self, msg, args):
        """post messages to social networks in one command

        !buffer post <network|all> <message> - add new post to deliver to social nework(s)

        network can be 'all' to publish to all social networks configured, or you can specify one of them,
        i.e.: facebook, twitter, gplus...
        """

        if len(args) < 3:
            return "usage: !buffer post <network|all> <message>"

        cmd = args[0]
        net = args[1]

        if net != "all" and net not in self.profiles:
            return "Network '%s' is not defined" % (net,)

        if cmd == "post":
            # instantiate the api object
            api = API(client_id=self.cid,
                      client_secret=self.cis,
                      access_token=self.apitoken)

            profiles = Profiles(api=api).all()

            for p in profiles:
                if net == "all" or p.id == self.profiles[net]:
                    p.updates.new(" ".join(args[2:]), now=True)

            return "Done. Published!"
        else:
            return "Sorry, I don't understand that command."
