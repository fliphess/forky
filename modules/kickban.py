#!/usr/bin/env python
"""
admin.py - bot Admin Module

"""
import re

from control.bot.decorators import commands, priority


auth_list = []
admins = []


def configure_host_mask(mask):
    if mask == '*!*@*':
        return mask

    if re.match(r'^[^.@!/]+$', mask) is not None:
        return '%s!*@*' % mask

    if re.match(r'^[^@!]+$', mask) is not None:
        return '*!*@%s' % mask

    m = re.match(r'^([^!@]+)@$', mask)
    if m is not None:
        return '*!%s@*' % m.group(1)

    m = re.match(r'^([^!@]+)@([^@!]+)$', mask)
    if m is not None:
        return '*!%s@%s' % (m.group(1), m.group(2))

    m = re.match(r'^([^!@]+)!(^[!@]+)@?$', mask)
    if m is not None:
        return '%s!%s@*' % (m.group(1), m.group(2))
    return ''


@commands('kick')
@priority('high')
def kick(bot, trigger):
    if not trigger.admin:
        return

    text = trigger.group().split()
    length = len(text)
    if length < 2:
        return

    opt = text[1]
    nick = opt
    channel = trigger.sender
    reason_idx = 2

    if opt.startswith('#'):
        if length < 3:
            return
        nick = text[2]
        channel = opt
        reason_idx = 3

    reason = ' '.join(text[reason_idx:])

    if nick != bot.settings.nick:
        bot.settings.log.info('Kicking %s on channel %s' % (nick, channel))
        bot.write(['KICK', channel, nick, reason])

@commands('ban')
@priority('high')
def ban(bot, trigger):
    """
        This give admins the ability to ban a user.
        The bot must be a Channel Operator for this command to work.
    """
    if not trigger.admin:
        return

    text = trigger.group().split()
    length = len(text)
    if length < 2:
        return

    opt = text[1]
    ban_mask = opt
    channel = trigger.sender

    if opt.startswith('#'):
        if length < 3:
            return
        channel = opt
        ban_mask = text[2]

    ban_mask = configure_host_mask(ban_mask)
    if ban_mask == '':
        return

    bot.settings.log.info('Banning %s from channel %s' % (ban_mask, channel))
    bot.write(['MODE %s +b %s' % (channel, ban_mask)])

@commands('unban')
@priority('high')
def unban(bot, trigger):
    """
        This give admins the ability to unban a user.
        The bot must be a Channel Operator for this command to work.
    """
    if not trigger.admin:
        return
    text = trigger.group().split()
    length = len(text)
    if length < 2:
        return

    opt = text[1]
    ban_mask = opt
    channel = trigger.sender

    if opt.startswith('#'):
        if length < 3:
            return
        channel = opt
        ban_mask = text[2]

    ban_mask = configure_host_mask(ban_mask)
    if ban_mask == '':
        return

    bot.settings.log.info('Removing ban for %s on channel %s' % (ban_mask, channel))
    bot.write(['MODE %s -b %s' % (channel, ban_mask)])


@commands('kickban', 'kb')
def kickban(bot, trigger):
    """ This gives admins the ability to kickban a user.
        The bot must be a Channel Operator for this command to work .kickban [#chan] user1 user!*@* get out of here
    """
    if not trigger.admin:
       return
    text = trigger.group().split()
    length = len(text)

    if length < 4:
        return

    opt = text[1]
    nick = opt
    mask = text[2]
    reason_idx = 3
    channel = ''

    if opt.startswith('#'):
        if length < 5:
            return
        channel = opt
        nick = text[2]
        mask = text[3]
        reason_idx = 4

    reason = ' '.join(text[reason_idx:])
    mask = configure_host_mask(mask)

    if mask == '':
        return

    bot.settings.log.info('Setting ban for %s on channel %s' % (nick, channel))
    bot.write(['MODE %s +b %s' % (channel, mask)])

    bot.settings.log.info('Kicking %s from channel %s' % (nick, channel))
    bot.write(['KICK %s %s  : %s' % (channel, nick, reason)])


if __name__ == '__main__':
    print __doc__
