"""

msg.py - bot messaging Module

"""
from control.bot.decorators import priority, rule, commands, thread, example

char_replace = {r'\x01': chr(1), r'\x02': chr(2), r'\x03': chr(3)}


@commands('msg')
@priority('low')
@example('.msg #YourPants Does anyone else smell neurotoxin?')
def msg(bot, trigger):
    """
    Send a message to a given channel or nick. Can only be done in privmsg by an
    admin.
    """
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return

    channel, _sep, message = trigger.group(2).partition(' ')
    message = message.strip()
    if not channel or not message:
        return
    bot.msg(channel, message)


@commands('me')
@priority('low')
def me(bot, trigger):
    """
    Send an ACTION (/me) to a given channel or nick. Can only be done in privmsg
    by an admin.
    """
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return

    channel, _sep, action = trigger.group(2).partition(' ')
    action = action.strip()
    if not channel or not action:
        return

    msg = '\x01ACTION %s\x01' % action
    bot.msg(channel, msg)


@commands('write')
@priority('high')
@thread(False)
def write_raw(bot, trigger):
    if not trigger.admin:
        return

    txt = trigger.bytes[7:]
    txt = txt.encode('utf-8')
    a = txt.split(':')
    status = False
    if len(a) > 1:
        newstr = u':'.join(a[1:])
        for x in char_replace:
            if x in newstr:
                newstr = newstr.replace(x, char_replace[x])
        bot.write(a[0].split(), newstr, raw=True)
        status = True
    elif a:
        b = a[0].split()
        bot.write([b[0].strip()], u' '.join(b[1:]), raw=True)
        status = True
    if status:
        bot.say('Message sent to server.')


@rule(r'($nickname!)')
@priority('high')
@example('$nickname!')
def respond(bot, trigger):
    """ Response to interjections
    """
    bot.say('Hi %s!' % trigger.nick)


@rule(r'(?i)$nickname[:,]?\sping')
@priority('high')
@example('$nickname: ping!')
def ping_respond(bot, trigger):
    """ Ping bot bot in a channel or pm
    """
    bot.reply('pong!')


if __name__ == '__main__':
    print __doc__
