#!/usr/bin/env python

from datetime import datetime
from subprocess import *

from control.bot.decorators import commands, priority, rate, rule


def git_info():
    p = Popen(['git', 'log', '-n 1'], stdout=PIPE, close_fds=True)
    commit = p.stdout.readline().strip()
    author = p.stdout.readline().strip()
    date = p.stdout.readline().strip()
    return commit, author, date


@commands('version')
@priority('medium')
@rate(10)
def version(bot, trigger):
    commit, author, date = git_info()
    nick = str(trigger.nick)
    bot.log.info('Sending version to %s' % nick)
    bot.say('%s: running version:' % nick)
    bot.say('  ' + commit.strip("\n"))
    bot.say('  ' + author.strip("\n"))
    bot.say('  ' + date.strip("\n"))


@rule('\x01VERSION\x01')
@rate(20)
def ctcp_version(bot, trigger):
    commit, author, date = git_info()
    date = date.replace('  ', '')
    bot.log.info('Replying to ctcp VERSION Trigger to %s' % trigger.nick)
    bot.write(('NOTICE', trigger.nick), '\x01VERSION {0} : {1}\x01'.format(commit, date))


@rule('\x01SOURCE\x01')
@rate(10)
def ctcp_source(bot, trigger):
    bot.log.info('Replying to ctcp SOURCE Trigger to %s' % trigger.nick)
    bot.write(('NOTICE', trigger.nick), '\x01SOURCE https://github.com/fliphess/forky/\x01')
    bot.write(('NOTICE', trigger.nick), '\x01SOURCE\x01')


@rule('\x01PING\s(.*)\x01')
@rate(10)
def ctcp_ping(bot, trigger):
    text = trigger.group()
    text = text.replace('PING ', '')
    text = text.replace('\x01', '')
    bot.log.info('Replying to ctcp PING Trigger to %s' % trigger.nick)
    bot.write(('NOTICE', trigger.nick), '\x01PING {0}\x01'.format(text))


@rule('\x01TIME\x01')
@rate(10)
def ctcp_time(bot, trigger):
    dt = datetime.now()
    current_time = dt.strftime('%A, %d. %B %Y %I:%M%p')
    bot.log.info('Replying to ctcp TIME Trigger to %s' % trigger.nick)
    bot.write(('NOTICE', trigger.nick), '\x01TIME {0}\x01'.format(current_time))


if __name__ == '__main__':
    print __doc__
