#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import requests

API_ROOT = "http://api.uptimerobot.com"

def human_status(status):
    if status == "0": return "PAUSED"
    if status == "1": return "PENDING"
    if status == "2": return "UP"
    if status == "8": return "DOWN"
    if status == "9": return "DOWN"

    return "UNKNOWN"


class UptimerobotMixin(object):

    def __init__(self, token):
        self.token = token

    def cmd_uptimerobot(self, msg, args):
        """!uptimerobot      - return the status of monitors in uptimerobot"""

        data = requests.get(API_ROOT + "/getMonitors", params={ "apiKey": self.token, "format": "json", "noJsonCallback": 1 }).json()

        ret=""
        for monitor in data["monitors"]["monitor"]:
            ret += "{status} {uptime}% {monitor}\n".format(
                    monitor=monitor["friendlyname"],
                    status=human_status(monitor["status"]),
                    uptime=monitor["alltimeuptimeratio"]
            )

        return str(ret)
