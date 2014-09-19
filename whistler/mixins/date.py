#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import time


class DateMixin(object):
    """Return the current date"""

    def cmd_date(self, msg, args):
        """!date [timezone] - return the current date in specified timezone or in UTC"""

        if len(args)>0:
            os.environ['TZ'] = " ".join(args)
            time.tzset()

        return str(time.strftime("%Y-%m-%d %H:%M:%S"))

