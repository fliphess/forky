#!/usr/bin/env python
"""
admin.py - bot Admin Module

"""
import re
from django.core.urlresolvers import reverse

from control.bot.decorators import commands, priority, restrict


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


@restrict(3)
@commands('kick')
@priority('high')
def kick(bot, trigger):
    if not trigger.admin:
        return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % reverse("registration_register"))

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
        bot.log.info('Kicking %s on channel %s' % (nick, channel))
        bot.write(['KICK', channel, nick, reason])


@restrict(3)
@commands('ban')
@priority('high')
def ban(bot, trigger):
    """
        This give admins the ability to ban a user.
        The bot must be a Channel Operator for this command to work.
    """
    if not trigger.admin:
        return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % reverse("registration_register"))

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

    bot.log.info('Banning %s from channel %s' % (ban_mask, channel))
    bot.write(['MODE %s +b %s' % (channel, ban_mask)])


@restrict(3)
@commands('unban')
@priority('high')
def unban(bot, trigger):
    """
        This give admins the ability to unban a user.
        The bot must be a Channel Operator for this command to work.
    """
    if not trigger.admin:
        return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % reverse("registration_register"))

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

    bot.log.info('Removing ban for %s on channel %s' % (ban_mask, channel))
    bot.write(['MODE %s -b %s' % (channel, ban_mask)])


@restrict(3)
@commands('kickban', 'kb')
@priority('high')
def kickban(bot, trigger):
    """ This gives admins the ability to kickban a user.
        The bot must be a Channel Operator for this command to work .kickban [#chan] user1 user!*@* get out of here
    """
    if not trigger.admin:
       return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % reverse("registration_register"))

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

    bot.log.info('Setting ban for %s on channel %s' % (nick, channel))
    bot.write(['MODE %s +b %s' % (channel, mask)])

    bot.log.info('Kicking %s from channel %s' % (nick, channel))
    bot.write(['KICK %s %s  : %s' % (channel, nick, reason)])


if __name__ == '__main__':
    print __doc__
