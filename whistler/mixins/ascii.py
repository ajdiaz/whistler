#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import requests

class AsciiMixin(object):
    """Return a text in ascii text"""

    def cmd_ascii(self, msg, args):
        """!ascii <text>   - return a text in ascii art font."""

        data = requests.get('http://asciime.heroku.com/generate_ascii', params={'s': " ".join(args)})

        return str("```%s``` " % (data.text,))


