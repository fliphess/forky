#!/usr/bin/env python
"""
    admin.py - bot Admin Module
"""
from django.conf import settings
from control.bot.decorators import commands, priority, example, restrict
from control.models import Channel


@restrict(1)
@commands('channels', 'list_channels')
@priority('low')
@example('.list_channels or .channels')
def list_channels(bot, trigger):
    if trigger.sender.startswith('#'):
        return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    if trigger.admin:
        channels = [i.channel for i in Channel.objects.all()]
        return bot.reply('Channels are: %s' % ", ".join(channels))


@restrict(3)
@commands('add_channel', 'join')
@priority('low')
@example('.add_channel #example')
def add_channel(bot, trigger):
    """ Join the specified channel. This is an admin-only command.
    """
    if trigger.sender.startswith('#') or not trigger.admin:
        return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    channel = trigger.group(3)
    key = trigger.group(4)

    if not channel or channel.startswith('#'):
        return

    bot.settings.log.info('Adding channel %s to database' % channel)
    obj, = Channel.objects.get_or_create(channel=channel)

    bot.settings.log.info('Joining channel %s' % channel)

    if not key:
        bot.write('JOIN', channel)
    else:
        bot.write('JOIN', channel, key)
        obj.key = key
    obj.save()
    bot.reply('Added and joined channel %s!' % channel)


@restrict(3)
@commands('remove_channel', 'part')
@priority('low')
@example('.remove_channel #example')
def remove_channel(bot, trigger):
    """ Part the specified channel. This is an admin-only command.
    """
    if trigger.sender.startswith('#') or not trigger.admin:
        return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    channel = trigger.group(3)
    if not channel or not channel.startswith('#'):
        return

    bot.settings.log.info('Disabling channel %s in database' % channel)
    Channel.objects.filter(channel=channel).delete()
    bot.settings.log.info('Leaving channel #%s' % channel)
    bot.reply('Leaving %s!' % channel)
    bot.write('PART', channel)


@restrict(2)
@commands('topic')
@priority('low')
def topic(bot, trigger):
    """ This gives admins the ability to change the topic.
        Note: One does *NOT* have to be an OP, one just has to be on the list of admins.
    """
    if not trigger.admin:
        return

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    channel = trigger.group(3)
    text = trigger.group(2)[1:]
    if not channel or not text:
        return

    bot.settings.log.info('Updating database!')
    ch, created = Channel.objects.get_or_create(channel=channel)
    ch.topic(text)
    ch.save()

    bot.settings.log.info('Settings topic for channel %s to %s' % (channel, text))
    bot.write('TOPIC %s %s' % (channel, text))


# TODO - Create topic trigger that sets the topic back when user != admin


if __name__ == '__main__':
    print __doc__

