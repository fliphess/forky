from peewee import DoesNotExist

from control.bot.decorators import example, priority, commands
from ircbot.models import InfoItem, start_db


@commands(['info'])
@priority('low')
@example('.info <item>')
def info(bot, trigger):
    try:
        item = trigger.group(2).split(' ')[0]
        start_db(bot.settings)
        obj = InfoItem.get(item=item)
    except (AttributeError, IndexError):
        return bot.reply('Usage: .info <item>')
    except DoesNotExist:
        bot.settings.log.info('Requested item "%s" not found!' % trigger.group(2))
        return bot.reply('Item "%s" not found!' % trigger.group(2))
    return bot.reply('[Item %s] %s: %s [last_modified: %s]' % (obj.id, obj.item, obj.text, obj.modified))


@commands(['add'])
@priority('low')
@example('.add <item> <text>')
def add(bot, trigger):
    try:
        incoming = trigger.group(2).split(' ')
        item = incoming[0]
        text = " ".join(incoming[1:])
    except (AttributeError, IndexError):
        return bot.reply('Usage: .add <item> <text>')

    try:
        start_db(bot.settings)
        obj = InfoItem.get(item=item)
        obj.text = "%s - %s" % (text, obj.text)
        obj.save()
        bot.settings.log.info('Requested item %s changed!' % item)
    except DoesNotExist:
        obj = InfoItem.create(
            item=item,
            text=text,
            creator_host=trigger.host,
            creator_nick=trigger.nick)
        obj.save()
        bot.settings.log.info('Requested item %s added!' % item)
        return bot.reply('Item %s added!' % item)


@commands(['update'])
@priority('low')
@example('.update <item> <text>')
def update(bot, trigger):
    try:
        incoming = trigger.group(2).split(' ')
        item = incoming[0]
        text = " ".join(incoming[1:])
    except (AttributeError, IndexError):
        return bot.reply('Usage: .add <item> <text>')

    try:
        start_db(settings=bot.settings)
        obj = InfoItem.get(item=item)
        obj.text = text
        obj.save()
        bot.settings.log.info('Requested item %s updated!' % item)
    except DoesNotExist:
        bot.settings.log.info('Item %s not found so not updated!' % item)
        return bot.reply('Item %s not found so not updated!' % item)
    return bot.reply('Item %s cupdated!' % item)


@commands(['delete'])
@priority('low')
@example('.delete <item>')
def delete(bot, trigger):
    try:
        item = trigger.group(2)
    except ValueError:
        return bot.reply('Usage: .delete <item>')

    start_db(bot.settings)
    q = InfoItem.delete().where(InfoItem.item == item)

    if q.execute():
        bot.settings.log.info('Requested item %s deleted!' % item)
        return bot.reply('Item %s deleted!' % item)

    bot.settings.log.info('Item %s not found so not deleted!' % item)
    return bot.reply('Item %s not found so not deleted!' % item)
