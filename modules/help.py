#!/usr/bin/env python
"""
help.py - forky Information Module
"""
from control.bot.decorators import priority, example, rule, commands


@rule('(?i)$nick[,:]\s(?:help|doc) +([A-Za-z]+)(?:\?+)?$')
@example('$nickname: doc tell?')
@priority('low')
def doc(bot, trigger):
    """ Shows a command's documentation, and possibly an example.
    """
    if trigger.group(1) == "help":
        name = trigger.group(2)
    else:
        name = trigger.group(1)
    name = name.lower()

    if name in bot.doc:
        bot.reply(bot.doc[name][0])
        if bot.doc[name][1]:
            bot.reply('e.g. ' + bot.doc[name][1])


@commands('commands', 'help')
@priority('low')
def commands(bot, trigger):
    """ This function only works in private message
    """
    if trigger.sender.startswith('#'):
        return

    if trigger.group(1) == "help" and trigger.group(2):
        doc(bot, trigger)
        return

    names = ', '.join(sorted(bot.doc.iterkeys()))
    bot.reply("I am sending you a private message of all my commands!")
    bot.msg(trigger.nick, 'Commands I recognise: %s' % names)


@rule(r'(?i)help(?:[?!]+)?$')
@priority('low')
def help(bot, trigger):
    response = "Hi, I'm a bot. Say \".commands\" to me in private for a list of my commands."
    bot.reply(response)


if __name__ == '__main__':
    print __doc__
