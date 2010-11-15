#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import xmpp
import threading


class WhistlerJob(threading.Thread):
    """ A generic job class, which calls a execute function each a specify
    number of seconds. This class will be extended to provide out-of-band
    actions for the bot. """


    def __init__(self, seconds=60, **kwargs):
        """ Create a new :class:`WhistlerJob` which calls the function
        :func:`execute` each *seconds*. This function will accept the same
        parameters as :class:`threading.Thread` does plus:

        :param `seconds`: which set the number of each seconds when
            execute function will be run. """

        super(WhistlerJob, self).__init__(**kwargs)
        self.cond = threading.Condition()
        self.halt = False
        self.seconds = seconds


    def run(self):
        """ The main thread running function, which calls :func:`execute`
        each *seconds* specify in :func:`__init__` function. """

        while not self.halt:
            self.cond.acquire()
            if not self.halt:
                self.execute()
                self.cond.wait(self.seconds)
            self.cond.release()


    def stop(self):
        """ Stop the job cleanly """

        self.cond.acquire()
        self.halt = True
        self.cond.notifyAll()
        self.cond.release()


    def execute(self):
        """ This function **must be** override to provide any action. This
        action will be executed each *seconds*, as specify in
        :func:`__init__` function. """

        raise NotImplementedError()


