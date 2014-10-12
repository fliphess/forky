from peewee import DoesNotExist

from control.bot.decorators import example, priority, commands
from ircbot.models import start_db, User


@commands(['about'])
@priority('low')
@example('.about <nick>')
def about(bot, trigger):
    try:
        nick = trigger.group(2).split()[0]
        start_db(settings=bot.settings)
        obj = User.get(nick=nick)
    except (AttributeError, IndexError):
        return bot.reply('Usage: .about <nick> <text>')
    except DoesNotExist:
        return bot.reply('User %s not found!' % trigger.group(2).split()[0])
    return bot.reply('[User %s]: %s [last_modified: %s][id: %s]' % (obj.nick, obj.about, obj.modified, obj.id))


@commands(['about_add'])
@priority('low')
@example('.about_add <nick> <text>')
def about_add(bot, trigger):
    try:
        incoming = trigger.group(2).split()
        nick = incoming[0]
        text = " ".join(incoming[1:])
        start_db(settings=bot.settings)
        obj = User.get(nick=nick)
    except (AttributeError, IndexError):
        return bot.reply('Usage: .about_add <nick> <text>')
    except DoesNotExist:
        return bot.reply('Nick %s not found! Use .adduser <nick> first.' % trigger.group(2).split()[0])

    if obj.about:
        obj.about = "%s - %s" % (text, obj.about)
    else:
        obj.about = text
    obj.save()
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
        start_db(settings=bot.settings)
        obj = User.get(nick=nick)
    except (AttributeError, IndexError):
        return bot.reply('Usage: .about_update <nick> <text>')
    except DoesNotExist:
        return bot.reply('Nick %s not found! Use .adduser <nick> first.' % trigger.group(2).split()[0])

    obj.about = text
    obj.save()
    msg = 'Requested data for %s updated!' % nick
    bot.settings.log.info(msg)
    return bot.reply(msg)
