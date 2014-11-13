from django.conf import settings
from django.core.urlresolvers import reverse
from control.bot.decorators import example, priority, commands, restrict
from items.models import InfoItem


@restrict(1)
@commands('info')
@priority('low')
@example('.info <item>')
def info(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        item = trigger.group(2).split(' ')[0]
        obj = InfoItem.objects.filter(item=item)
    except (AttributeError, IndexError):
        return bot.reply('Usage: .info <item>')

    if not obj:
        bot.log.info('Requested item "%s" not found!' % trigger.group(2))
        return bot.reply('Item "%s" not found!' % trigger.group(2))
    obj = obj[0]
    return bot.reply('[Item %s] %s' % (obj.item, obj.text))


@restrict(1)
@commands('add')
@priority('low')
@example('.add <item> <text>')
def add(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        incoming = trigger.group(2).split(' ')
        item = incoming[0]
        text = " ".join(incoming[1:])
    except (AttributeError, IndexError):
        return bot.reply('Usage: .add <item> <text>')

    obj, created = InfoItem.objects.get_or_create(item=item)
    if obj.text:
        obj.text = "%s - %s" % (text, obj.text)
    else:
        obj.text = text

    obj.save()
    bot.log.info('Requested item %s changed!' % item)
    obj.save()
    bot.log.info('Requested item %s added!' % item)
    return bot.reply('Item %s added!' % item)


@restrict(1)
@commands('update')
@priority('low')
@example('.update <item> <text>')
def update(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        incoming = trigger.group(2).split(' ')
        item = incoming[0]
        text = " ".join(incoming[1:])
    except (AttributeError, IndexError):
        return bot.reply('Usage: .add <item> <text>')

    obj = InfoItem.objects.filter(item=item)
    if obj:
        obj = obj[0]
        obj.text = text
        obj.save()
        bot.log.info('Requested item %s updated!' % item)
    else:
        bot.log.info('Item %s not found so not updated!' % item)
        return bot.reply('Item %s not found so not updated!' % item)
    return bot.reply('Item %s updated!' % item)


@restrict(1)
@commands('delete')
@priority('low')
@example('.delete <item>')
def delete(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        item = trigger.group(2)
    except ValueError:
        return bot.reply('Usage: .delete <item>')

    obj = InfoItem.objects.filter(item=item)
    if not obj:
        msg = 'Item %s not found so not deleted!' % item
        bot.log.info(msg)
        return bot.reply(msg)

    if obj[0].delete():
        bot.log.info('Requested item %s deleted!' % item)
        return bot.reply('Item %s deleted!' % item)
    else:
        bot.log.info('[ERROR] Requested item %s somehow not deleted!' % item)
        return bot.reply('[ERROR] Item %s somehow not deleted!' % item)
