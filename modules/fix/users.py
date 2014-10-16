from django.core.urlresolvers import reverse
from control.bot.decorators import commands, example, priority


@commands('adduser', 'meet')
@priority('low')
@example('.meet <nick>')
def meet(bot, trigger):
    if trigger.sender.startswith('#') or not trigger.admin:
        return
    bot.msg(trigger.group(3), 'You can register yourself at: %s' % reverse("registration_register"))


@commands('verify', 'register')
@priority('low')
@example('.verify <token>')
def login(bot, trigger):
    if trigger.sender.startswith('#'):
        # TODO - lock account because of public message
        return


def register(bot, trigger):
    if trigger.sender.startswith('#'):
        # TODO - lock account because of public message
        return
