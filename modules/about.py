from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from control.bot.decorators import example, priority, commands

BotUser = get_user_model()

@commands(['about'])
@priority('low')
@example('.about <nick>')
def about(bot, trigger):
    nick = trigger.group(2).split()[0]
    user = BotUser.objects.filter(nick=nick)
    if not user:
        return bot.reply('User %s not found!' % trigger.group(2).split()[0])
    user = user[0]
    return bot.reply('[About %s]: %s' % (user.username, user.about))


@commands(['about_add'])
@priority('low')
@example('.about_add <nick> <text>')
def about_add(bot, trigger):
    if not trigger.user_object and not trigger.user.registered:
        return bot.msg(trigger.nick, 'Please register first at %s' % reverse("registration_register"))

    try:
        incoming = trigger.group(2).split()
        nick = incoming[0]
        text = " ".join(incoming[1:])
    except (AttributeError, IndexError):
        return bot.reply('Usage: .about_add <nick> <text>')

    user = BotUser.objects.filter(nick=nick)
    if not user:
        return bot.reply('Nick %s not found! Use .adduser <nick> first.' % trigger.group(2).split()[0])

    user = user[0]
    if user.about:
        user.about = "%s - %s" % (text, user.about)
    else:
        user.about = text
    user.save()
    msg = 'Requested data for %s added!' % nick
    bot.settings.log.info(msg)
    return bot.reply(msg)


@commands(['about_update'])
@priority('low')
@example('.about_update <nick> <text>')
def about_update(bot, trigger):
    try:
        incoming = trigger.group(2).split()
        nick = incoming[0]
        text = " ".join(incoming[1:])
    except (AttributeError, IndexError):
        return bot.reply('Usage: .about_update <nick> <text>')

    user = BotUser.objects.filter(nick=nick)
    if not user:
        return bot.reply('Nick %s not found! Use .adduser <nick> first.' % trigger.group(2).split()[0])
    user = user[0]
    user.about = text
    user.save()
    msg = 'Requested data for %s updated!' % nick
    bot.settings.log.info(msg)
    return bot.reply(msg)
