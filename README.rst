============
Whistler Bot
============

Whistler Bot is an XMPP bot written in python using pyxmpp, which is
a requirement. The bot is designed to handle some commands, and it's easy to
extend.

Simple usage::

    from whistler.bot import WhistlerBot

    bot = WhistlerBot( "myjid@myserver.com", "mypassword" )
    bot.start()

The provided console script called ``whistler`` is a single bot which reply
to a ``!ping`` command.


Extending bot
-------------

You can extend the bot functionalities, just see for example the code of the
whistler console script. In short you can add commands creating a new class
from WhistlerBot, and define new functions in the form *cmd_* plus the
command name, for example, to handle the command *ping*::

    from whistler.bot import WhistlerBot

    class MyBot(WhistlerBot):

        def cmd_ping(self, msg, args):
            return "pong"

Enjoy!

