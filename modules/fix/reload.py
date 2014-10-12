#!/usr/bin/env python
from imp import load_source
import os
import sys
from control.bot.decorators import commands, priority, thread
from django_ircbot.models import Module


@commands(['reload'])
@priority('low')
@thread(False)
def f_reload(bot, trigger):
    """ Reloads all modules, for use by admins only.
    """
    if trigger.sender.startswith('#'):
        return

    if not trigger.admin:
        return

    modules = []
    files = [i.filename for i in Module.objects.filter(enabled=True)]

    for filename in files:
        name = os.path.basename(filename)[:-3]
        try:
            module = load_source(name, filename)
        except ImportError as e:
            bot.log.error("Error loading %s: %s (in %s)" % (name, e, filename))
        if hasattr(module, 'setup'):
            module.setup(bot)
        bot.register(vars(module))
        modules.append(name)

    if modules:
        bot.log.debug('Registered modules: %s' % ', '.join(modules))
        bot.modules = modules
    else:
        bot.log.error("Warning: Couldn't find any modules")
    bot.bind_commands()

    msg = 'RELOADED: %r -- (%s)' % (", ".join(modules), trigger.nick)
    bot.say(msg)
    bot.log.debug(msg)
