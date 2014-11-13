from django.conf import settings
from control.bot.decorators import commands, example, priority, restrict


@restrict(1)
@commands('adduser', 'meet')
@priority('low')
@example('.meet <nick>')
def meet(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    bot.msg(trigger.group(3), 'Hi %s! You can register yourself at: %s' % (trigger.group(3), settings.FULL_URL))


@restrict(0)
@commands('login', 'verify')
@priority('low')
@example('/msg %s .login <token>' % settings.BOT_NICK)
def login(bot, trigger):
    if trigger.sender.startswith('#'):
        trigger.user_object.disable_account()
        return bot.reply('I Disabled your account because of in-channel login. '
                         'Please ask a moderator to re-enable!')
    token = trigger.group(3)
    if not token:
        return bot.reply('Usage /msg %s .login <token>' % settings.BOT_NICK)
    if token == trigger.user_object.registration_token:
        trigger.user_object.login_user()
        trigger.user_object.renew_token()
        bot.reply('You are now logged in!')


@commands('register')
@priority('low')
@example('/msg %s .register <token>' % settings.BOT_NICK)
def register(bot, trigger):
    if trigger.sender.startswith('#'):
        trigger.user_object.disable_account()
        return bot.reply('I Disabled your account because of in-channel login. '
                         'Please ask a moderator to re-enable!')
    token = trigger.group(3)
    if not token:
        return bot.reply('Usage /msg %s .register <token>' % settings.BOT_NICK)
    if token == trigger.user_object.registration_token:
        trigger.user_object.register_user()
        trigger.user_object.renew_token()
        bot.reply('You are now registered!')


@commands('status')
@priority('low')
@example('.status')
def status(bot, trigger):
    bot.reply('Your status is %s' % trigger.status)
