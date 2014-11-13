from django.conf import settings
from control.bot.decorators import example, priority, commands, restrict
from items.models import Quote

@restrict(1)
@priority('low')
@commands('quote')
@example('.quote')
def quote(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        q = Quote.objects.order_by('?')[0]
    except (AttributeError, IndexError):
        return bot.reply('Usage: .info')

    if not q:
        return bot.reply('No quotes found for %s!' % trigger.nick)
    return bot.reply('[%s] Random quote: %s - %s [%s]' % (trigger.nick, q.text, q.date_added, q.id))


@restrict(1)
@priority('low')
@commands('add_quote')
@example('.add_quote <text>')
def add_quote(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    text = trigger.group(2)
    obj, created = Quote.objects.get_or_create(user=trigger.user_object, quote=text)
    obj.save()

    bot.log.info('Requested quote %s with id %s saved for user %s!' % (obj.id, quote, trigger.user_object.username))
    return bot.reply('Quote added for %s with id %s: %s!' % (trigger.nick, obj.id, text))


@restrict(1)
@commands('delete_quote')
@priority('low')
@example('.delete_quote <id>')
def delete(bot, trigger):
    if not trigger.user_object or not trigger.user_object.is_login or not trigger.user_object.registered:
        return bot.msg(trigger.nick, 'Please login or register first at %s' % settings.FULL_URL)

    try:
        quote_id = int(trigger.group(2))
        obj = Quote.objects.get(user__username=trigger.user_object.username, id=quote_id)
    except (ValueError, Quote.DoesNotExist):
        return bot.reply('Usage: .delete <quote id>')

    if obj.delete():
        bot.log.info('Requested quote %s deleted!' % quote)
        return bot.reply('Item %s deleted!' % quote)
    else:
        bot.log.info('[ERROR] Requested quote %s somehow not deleted!' % quote_id)
        return bot.reply('[ERROR] Item %s somehow not deleted!' % quote_id)
