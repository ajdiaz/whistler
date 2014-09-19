#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


import hashlib

class HashMixin(object):
    """Return the hexadecimal hash code of a string"""

    def cmd_hash(self, msg, args):
        """!hash <md5|sha1|ripemd16|sha256...> <text>   - return the hash of a text."""

        if len(args) < 2:
            return "Sorry, I need algorithm and text"

        try:
            h = hashlib.new(args[0])
        except:
            return "Sorry I do not known that algorithm."
        h.update(" ".join(args[1:]))

        return str(h.hexdigest())


