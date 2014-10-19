from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from control.bot.decorators import example, priority, commands, restrict
BotUser = get_user_model()


@restrict(1)
@commands('about')
@priority('low')
@example('.about <nick>')
def about(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % reverse("registration_register"))

    try:
        incoming = trigger.group(2).split()
        nick = incoming[0]
    except (AttributeError, IndexError):
        return bot.reply('Usage: .about_add <nick> <text>')
    user = BotUser.objects.filter(nick=nick)
    if user:
        user = user[0]
        return bot.reply('[About %s]: %s' % (user.username, user.about))
    return bot.reply('User %s not found!' % trigger.group(2).split()[0])


@restrict(1)
@commands('about_add')
@priority('low')
@example('.about_add <nick> <text>')
def about_add(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % reverse("registration_register"))

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
    bot.log.info(msg)
    return bot.reply(msg)


@restrict(1)
@commands('about_update')
@priority('low')
@example('.about_update <nick> <text>')
def about_update(bot, trigger):
    if not trigger.user_object and not trigger.user_object.is_login:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % reverse("registration_register"))
    try:
        incoming = trigger.group(2).split()
        nick = incoming[0]
        text = " ".join(incoming[1:])
    except (AttributeError, IndexError):
        return bot.reply('Usage: .about_update <nick> <text>')

    user = trigger.user_object
    if not user:
        return bot.reply('Nick %s not found! Use .adduser <nick> first.' % trigger.group(2).split()[0])
    user.about = text
    user.save()
    msg = 'Requested data for %s updated!' % nick
    bot.log.info(msg)
    return bot.reply(msg)
