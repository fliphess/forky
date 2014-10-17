from django.core.urlresolvers import reverse
from control.bot.decorators import commands, example, priority, restrict


@restrict(1)
@commands('adduser', 'meet')
@priority('low')
@example('.meet <nick>')
def meet(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    bot.msg(trigger.group(3), 'You can register yourself at: %s' % reverse("registration_register"))


@restrict(0)
@commands('login', 'verify')
@priority('low')
@example('.login <token>')
def login(bot, trigger):
    if trigger.sender.startswith('#'):
        trigger.user_object.disable_account()
        return bot.reply('Disabled your account because of in-channel login. Please ask a moderator to re-enable!')
    token = trigger.group(3)
    if not token:
        return bot.reply('Usage .login <token>')
    if token == trigger.user_object.registration_token:
        trigger.user_object.login_user()
        trigger.user_object.renew_token()
        bot.reply('You are now login!')

@restrict(1)
@commands('login', 'verify')
@priority('low')
@example('.login <token>')
def login(bot, trigger):
    if trigger.sender.startswith('#'):
        trigger.user_object.disable_account()
        return bot.reply('Disabled your account because of in-channel login. Please ask a moderator to re-enable!')
    token = trigger.group(3)
    if not token:
        return bot.reply('Usage .login <token>')
    if token == trigger.user_object.registration_token:
        trigger.user_object.login_user()
        trigger.user_object.renew_token()
        bot.reply('You are now login!')


@commands('register')
@priority('low')
@example('.register <token>')
def register(bot, trigger):
    if trigger.sender.startswith('#'):
        trigger.user_object.disable_account()
        return bot.reply('Disabled your account because of in-channel login. Please ask a moderator to re-enable!')
    token = trigger.group(3)
    if not token:
        return bot.reply('Usage .register <token>')
    if token == trigger.user_object.registration_token:
        trigger.user_object.register_user()
        trigger.user_object.renew_token()
        bot.reply('You are now registered!')


@commands('status')
@priority('low')
@example('.verify <token>')
def status(bot, trigger):
    bot.reply('Your status is %s' % trigger.status)
