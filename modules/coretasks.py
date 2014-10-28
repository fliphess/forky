# coding=utf-8
from django.conf import settings
from django.contrib.auth import get_user_model
from control.bot.decorators import event, rule, priority, commands, restrict
from profile.models import Channel
BotUser = get_user_model()

@event('251')
@rule('.*')
@priority('low')
def startup(bot, trigger):
    """
    Runs when we recived 251 - lusers, which is just before the server sends the
    motd, and right after establishing a sucessful connection.
    """
    if (hasattr(settings, 'IRC_OPER_NAME') and hasattr(settings, 'IRC_OPER_PASSWORD') and
                settings.IRC_OPER_NAME is not None and settings.IRC_OPER_PASSWORD is not None):
        bot.write(('OPER', '%s %s' % (settings.IRC_OPER_NAME, settings.IRC_OPER_PASSWORD)))

        if hasattr(settings, 'IRC_OPER_MODES'):
            modes = settings.IRC_OPER_MODES
        else:
            modes = 'B'
        bot.write(('MODE', '%s +%s' % (bot.nick, modes)))

    channels = [i.channel for i in Channel.objects.all()]
    for channel in channels:
        bot.log.info('Rejoining channel %s' % channel)
        bot.write(('JOIN', channel))


@restrict(0)
@commands('listops')
def list_ops(bot, trigger):
    """ List channel operators in the given channel, or current channel if none is given.
    """
    ops = [i.nick for i in BotUser.objects.filter(is_operator=True)]
    if not ops:
        bot.say('No operators defined in DB!')
    else:
        bot.say('I have %s registered operators in my database: %s' % (len(ops), ", ".join(ops)))


@restrict(0)
@commands('listvoices')
def list_voices(bot, trigger):
    """ List users with voice in the given channel, or current channel if none is given.
    """
    voice = [i.nick for i in BotUser.objects.filter(is_voice=True)]
    if not voice:
        bot.say('No half ops defined in DB!')
    else:
        bot.say('I have %s registered halfops (voice) in my database: %s' % (len(voice), ", ".join(voice)))


@rule('.*')
@event('NICK')
def track_bot_nick_changes(bot, trigger):
    """ Track nickname changes """
    if trigger.nick == bot.nick:
        debug_msg = "Nick changed by server. This can cause unexpected behavior. Please restart the bot."
        bot.log.warn(debug_msg)
        return


@event('KICK')
@rule('.*')
@priority('high')
def auto_rejoin_on_kick(bot, trigger):
    """ This function monitors all kicks across all channels bot is in. If she
    detects that she is the one kicked she'll automatically join that channel.

    WARNING: This may not be needed and could cause problems if bot becomes
    annoying. Please use this with caution.
    """
    channel = trigger.sender
    bot.log.info('Kicked from %s! Rejoining' % channel)
    bot.write('JOIN', channel)
