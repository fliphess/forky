from control.bot.decorators import commands, example, priority


@commands('adduser', 'meet')
@priority('low')
@example('.meet <nick> <email>')
def meet(bot, trigger):
    if trigger.sender.startswith('#') or not trigger.admin:
        return

    # TODO - Extend django usermodel
    # TODO - Create user
    # TODO - send verification email
    # Create User
    # Generate OTP


@commands('verify', 'register')
@priority('low')
@example('.verify <token>')
def verify(bot, trigger):
    if not trigger.admin:
        return
    if trigger.sender.startswith('#'):
        # TODO - lock account because of public message
        return

