from django.conf import settings
from django.core.urlresolvers import reverse
from control.bot.decorators import example, priority, commands, restrict


@restrict(3)
@commands('voice')
@priority('low')
@example('.voice #example or .voice #example nick')
def voice(bot, trigger):
    """Command to voice users in a room. If no nick is given, bot will voice the nick who sent the command
    """
    if not trigger.admin:
        return bot.reply('You must be an admin to perform this operation')

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        inputs = trigger.group(2).split(' ')
    except (IndexError, AttributeError):
        return bot.reply('Invalid input: .voice #example or .voice #example nick')

    try:
        channel = inputs[0]
        if not channel.startswith('#'):
            raise TypeError
    except (IndexError, TypeError):
        return bot.reply('You must provide a valid channel')

    nick = None
    try:
        nick = inputs[1]
    except (TypeError, IndexError):
        pass

    if not nick:
        nick = trigger.nick
    bot.log.info('Giving voice on %s from %s' % (channel, nick))
    bot.write(['MODE %s +v %s' % (channel, nick)])


@restrict(3)
@commands('devoice')
@priority('low')
@example('.devoice #example or .devoice #example nick')
def devoice(bot, trigger):
    """ Command to devoice users in a room. If no nick is given, bot will devoice the nick who sent the command
    """
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    if not trigger.admin:
        return bot.reply('You must be an admin to perform this operation')

    try:
        inputs = trigger.group(2).split(' ')
    except (IndexError, AttributeError):
        return bot.reply('Invalid input: .devoice #example or .devoice #example nick')

    try:
        channel = inputs[0]
        if not channel.startswith('#'):
            raise TypeError
    except (IndexError, TypeError):
        return bot.reply('You must provide a valid channel')

    nick = None
    try:
        nick = inputs[1]
    except (TypeError, IndexError):
        pass

    if not nick:
        nick = trigger.nick
    bot.log.info('Removing voice on %s from %s' % (channel, nick))
    bot.write(['MODE %s -v %s' % (channel, nick)])



@restrict(3)
@commands('op')
@priority('low')
@example('.op #example or .op #example nick')
def op(bot, trigger):
    """ Command to op users in a room. If no nick is given, bot will op the nick who sent the command
    """
    if not trigger.admin:
        return bot.reply('You must be an admin to perform this operation')

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        inputs = trigger.group(2).split(' ')
    except (IndexError, AttributeError):
        return bot.reply('Invalid input: .op #example or .op #example nick')

    try:
        channel = inputs[0]
    except (IndexError, TypeError):
        return bot.reply('You must provide a valid channel')

    if not channel.startswith('#'):
        return

    nick = None
    try:
        nick = inputs[1]
    except (TypeError, IndexError):
        pass

    if not nick:
        nick = trigger.nick
    bot.log.info('Giving ops on %s to %s' % (channel, nick))
    bot.write(['MODE %s +o %s' % (channel, nick)])


@restrict(3)
@commands('deop')
@priority('low')
@example('.deop #example or .deop #example nick')
def deop(bot, trigger):
    """ Command to deop users in a room. If no nick is given, bot will deop the nick who sent the command
    """
    if not trigger.admin:
        return bot.reply('You must be an admin to perform this operation')

    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        inputs = trigger.group(2).split(' ')
    except (IndexError, AttributeError):
        return bot.reply('Invalid input: .deop #example or .deop #example nick')

    try:
        channel = inputs[0]
        if not channel.startswith('#'):
            raise TypeError
    except (IndexError, TypeError):
        return bot.reply('You must provide a valid channel')

    nick = None
    try:
        nick = inputs[1]
    except (TypeError, IndexError):
        pass

    if not nick:
        nick = trigger.nick
    bot.log.info('Removing ops on %s from %s' % (channel, nick))
    bot.write(['MODE %s -o %s' % (channel, nick)])

