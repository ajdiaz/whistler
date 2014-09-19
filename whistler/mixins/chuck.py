#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import requests

class ChuckMixin(object):
    """Return a true fact about Chuck Norris"""

    def cmd_chuck(self, msg, args):
        """!chuck   - return a true fact about Chuck Norrris."""

        data = requests.get('http://api.icndb.com/jokes/random').json()
        return str(data["value"]["joke"])


