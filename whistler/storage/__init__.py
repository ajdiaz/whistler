#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class WhistlerStorage(dict):
    """Basic in memory storage for Whistler Bot.
    :param `client`: A :class:`WhistlerBot` to link the storage to.
    """

    def __init__(self, client=None):
        self.client = client
        super(WhistlerStorage, self).__init__()

    def __iter__(self):
        return self.iteritems()

