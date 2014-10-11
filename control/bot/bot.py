# coding=utf-8
"""
bot.py - Willie IRC Bot
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright 2012, Edward Powell, http://embolalia.net
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>

Licensed under the Eiffel Forum License 2.

http://ircbot.dftba.net/
"""
from imp import load_source
import os

import time
import re
import threading
from datetime import datetime
import sys
from tabulate import tabulate
from django import setup as django_setup

sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control.settings")
django_setup()

from django_ircbot.exceptions import BotException
from django_ircbot.models import Module, BotUser
import irc
from tools import PriorityQueue, Released, get_command_regexp, BotMemory


class DjangoBot(irc.Bot):
    def __init__(self):
        irc.Bot.__init__(self)
        self.doc = {}
        self.times = {}
        self.callables = set()
        self.commands = {'high': {}, 'medium': {}, 'low': {}}
        self.memory = BotMemory()
        self.scheduler = DjangoBot.JobScheduler(self)
        self.scheduler.start()
        self.setup()

    class JobScheduler(threading.Thread):
        """ Calls jobs assigned to it in steady intervals.

        JobScheduler is a thread that keeps track of Jobs and calls them
        every X seconds, where X is a property of the Job. It maintains jobs
        in a priority queue, where the next job to be called is always the
        first item. Thread safety is maintained with a mutex that is released
        first item. Thread safety is maintained with a mutex that is released
        during long operations, so methods add_job and clear_jobs can be
        safely called from the main thread.
        """
        min_reaction_time = 30.0
        """ How often should scheduler checks for changes in the job list."""

        def __init__(self, bot):
            """ Requires bot as argument for logging. """
            threading.Thread.__init__(self)
            self.bot = bot
            self._jobs = PriorityQueue()
            self._mutex = threading.Lock()
            self._cleared = False

        def add_job(self, job):
            """ Add a Job to the current job queue."""
            self._jobs.put(job)

        def clear_jobs(self):
            """Clear current Job queue and start fresh."""
            if self._jobs.empty():
                return
            with self._mutex:
                self._cleared = True
                self._jobs = PriorityQueue()

        def run(self):
            """ Run forever. """
            while True:
                try:
                    self._do_next_job()
                except Exception:
                    self.bot.error()
                    time.sleep(10.0)

        def _do_next_job(self):
            """Wait until there is a job and do it."""
            with self._mutex:
                while True:
                    job = self._jobs.peek()
                    difference = job.next_time - time.time()
                    duration = min(difference, self.min_reaction_time)
                    if duration <= 0:
                        break
                    with Released(self._mutex):
                        time.sleep(duration)

                self._cleared = False
                job = self._jobs.get()
                with Released(self._mutex):
                    if job.func.thread:
                        t = threading.Thread(
                                target=self._call, args=(job.func,))
                        t.start()
                    else:
                        self._call(job.func)
                    job.next()
                if not self._cleared:
                    self._jobs.put(job)

        def _call(self, func):
            """ Wrapper for collecting errors from modules. """
            # Willie.bot.call is way too specialized to be used instead.
            try:
                func(self.bot)
            except Exception:
                self.bot.error()

    class Job(object):
        """ Job is a simple structure that hold information about when a function
        should be called next. They can be put in a priority queue, in which case
        the Job that should be executed next is returned.

        Calling the method next modifies the Job object for the next time it should
        be executed. Current time is used to decide when the job should be executed
        next so it should only be called right after the function was called.
        """

        max_catchup = 5
        """ This governs how much the scheduling of jobs is allowed to get behind
        before they are simply thrown out to avoid calling the same function too
        many times at once.
        """

        def __init__(self, interval, func):
            """ Initialize Job.

            Args:
                interval: number of seconds between calls to func
                func: function to be called
            """
            self.next_time = time.time() + interval
            self.interval = interval
            self.func = func

        def next(self):
            """ Update self.next_time with the assumption func was just called.
                Returns: A modified job object.
            """
            last_time = self.next_time
            current_time = time.time()
            delta = last_time + self.interval - current_time

            if last_time > current_time + self.interval:
                # Clock appears to have moved backwards. Reset the timer to avoid
                # waiting for the clock to catch up to whatever time it was
                # previously.
                self.next_time = current_time + self.interval
            elif delta < 0 and abs(delta) > self.interval * self.max_catchup:
                # Execution of jobs is too far behind. Give up on trying to catch
                # up and reset the time, so that will only be repeated a maximum
                # of self.max_catchup times.
                self.next_time = current_time - self.interval * self.max_catchup
            else:
                self.next_time = last_time + self.interval
            return self

        def __cmp__(self, other):
            """Compare Job objects according to attribute next_time."""
            return self.next_time - other.next_time

        def __str__(self):
            """Return a string representation of the Job object.

            Example result:
                <Job(2013-06-14 11:01:36.884000, 20s, <function upper at 0x02386BF0>)>
            """
            iso_time = str(datetime.fromtimestamp(self.next_time))
            return "<Job(%s, %ss, %s)>" % \
                (iso_time, self.interval, self.func)

        def __iter__(self):
            """This is an iterator. Never stops though."""
            return self

    def setup(self):
        self.log.info("\nWelcome to Django IRC Bot. Loading modules...\n\n")
        modules = []
        error_count = 0

        for item in Module.objects.filter(enabled=True):
            try:
                module = load_source(item.name, item.filename)
            except (IOError, ImportError) as e:
                error_count += 1
                self.log.error("Error loading %s: %s (in %s)" % (item.name, e, item.filename))
            else:
                try:
                    if hasattr(module, 'setup'):
                        module.setup(self)
                    self.register(vars(module))
                    modules.append(item.name)
                except Exception as e:
                    error_count += 1
                    self.log.error("Error in %s setup procedure: %s (in %s)" % (item.name, e, item.filename))

        if modules:
            self.log.info('\n\nRegistered %d modules,' % (len(modules) - 1))
            self.log.info('%d modules failed to load\n\n' % error_count)
        else:
            self.log.error("Warning: Couldn't find any modules")
        self.bind_commands()

    @staticmethod
    def is_callable(obj):
        if not callable(obj):
            return False
        if (hasattr(obj, 'commands') or
                hasattr(obj, 'rule') or
                hasattr(obj, 'interval')):
            return True
        return False

    def register(self, variables):
        for obj in variables.itervalues():
            if self.is_callable(obj):
                self.callables.add(obj)

    def unregister(self, variables):
        def remove_func(func, commands):
            """ Remove all traces of func from commands. """
            for func_list in commands.itervalues():
                if func in func_list:
                    func_list.remove(func)
        
        for obj in variables.itervalues():
            if not self.is_callable(obj):
                continue
            if obj in self.callables:
                self.callables.remove(obj)
                for commands in self.commands.itervalues():
                    remove_func(obj, commands)

    def bind_commands(self):
        self.scheduler.clear_jobs()
        table = []

        def bind(self, priority, regexp, func):
            table.append([func.__name__.encode('ascii'), "LOADED", regexp.pattern.encode('ascii'), priority])

            if not hasattr(func, 'name'):
                func.name = func.__name__

            if func.__doc__ and hasattr(func, 'commands') and func.commands[0]:
                if hasattr(func, 'example'):
                    if isinstance(func.example, basestring):
                        example = func.example
                    else:
                        example = func.example[0]["example"]
                    example = example.replace('$nickname', str(self.nick))
                else:
                    example = None
                self.doc[func.commands[0]] = (func.__doc__, example)
            self.commands[priority].setdefault(regexp, []).append(func)

        def sub(pattern, self=self):
            pattern = pattern.replace('$nickname', r'%s' % re.escape(self.nick))
            return pattern.replace('$nick', r'%s[,:] +' % re.escape(self.nick))

        for func in self.callables:
            if not hasattr(func, 'priority'):
                func.priority = 'medium'

            if not hasattr(func, 'thread'):
                func.thread = True

            if not hasattr(func, 'event'):
                func.event = 'PRIVMSG'
            else:
                func.event = func.event.upper()

            if not hasattr(func, 'rate'):
                if hasattr(func, 'commands'):
                    func.rate = 0
                else:
                    func.rate = 0

            if hasattr(func, 'rule'):
                rules = func.rule
                if isinstance(rules, basestring):
                    rules = [func.rule]

                if isinstance(rules, list):
                    for rule in rules:
                        pattern = sub(rule)
                        flags = re.IGNORECASE
                        if rule.find("\n") != -1:
                            flags |= re.VERBOSE
                        regexp = re.compile(pattern, flags)
                        bind(self, func.priority, regexp, func)

                elif isinstance(func.rule, tuple):
                    # 1) e.g. ('$nick', '(.*)')
                    if len(func.rule) == 2 and isinstance(func.rule[0], str):
                        prefix, pattern = func.rule
                        prefix = sub(prefix)
                        regexp = re.compile(prefix + pattern, re.I)
                        bind(self, func.priority, regexp, func)

                    # 2) e.g. (['p', 'q'], '(.*)')
                    elif len(func.rule) == 2 and isinstance(func.rule[0], list):
                        prefix = settings.BOT_PREFIX
                        commands, pattern = func.rule
                        for command in commands:
                            command = r'(%s)\b(?: +(?:%s))?' % (command, pattern)
                            regexp = re.compile(prefix + command, re.I)
                            bind(self, func.priority, regexp, func)

                    # 3) e.g. ('$nick', ['p', 'q'], '(.*)')
                    elif len(func.rule) == 3:
                        prefix, commands, pattern = func.rule
                        prefix = sub(prefix)
                        for command in commands:
                            command = r'(%s) +' % command
                            regexp = re.compile(prefix + command + pattern, re.I)
                            bind(self, func.priority, regexp, func)

            if hasattr(func, 'commands'):
                for command in func.commands:
                    prefix = settings.BOT_PREFIX
                    regexp = get_command_regexp(prefix, command)
                    bind(self, func.priority, regexp, func)

            if hasattr(func, 'interval'):
                for interval in func.interval:
                    job = DjangoBot.Job(interval, func)
                    self.scheduler.add_job(job)
        if table:
            self.log.info("\n" + tabulate(table, headers=["Name", "Status", "Regex", "Priority"], tablefmt='grid'))

    class BotWrapper(object):
        def __init__(self, willie, origin):
            self.bot = willie
            self.origin = origin

        def say(self, string, max_messages=1):
            self.bot.msg(self.origin.sender, string, max_messages)

        def reply(self, string):
            if isinstance(string, str):
                string = string.decode('utf8')
            self.bot.msg(self.origin.sender, u'%s: %s' % (self.origin.nick, string))

        def action(self, string, recipient=None):
            if recipient is None:
                recipient = self.origin.sender
            self.bot.msg(recipient, '\001ACTION %s\001' % string)

        def __getattr__(self, attr):
            return getattr(self.bot, attr)

    class Trigger(unicode):
        def __new__(cls, text, origin, bytes, match, event, args, self):
            s = unicode.__new__(cls, text)
            user = BotUser.objects.filter(nick=origin.nick, host=origin.hostmask)

            if user:
                s.user_object = user[0]
                s.registered = True
                s.admin = s.user_object.admin
            else:
                s.user_object = False
                s.registered = False
                s.admin = False

            s.sender = origin.sender
            s.hostmask = origin.hostmask
            s.user = origin.user
            s.nick = origin.nick
            s.event = event
            s.bytes = bytes
            s.match = match
            s.group = match.group
            s.groups = match.groups
            s.args = args
            s.host = origin.host

            if s.sender is not s.nick:  # no ops in PM
                s.isop = s.user_object.operator
                s.isvoice = s.user_object.voice
                s.isbanned = s.user_object.banned
            else:
                s.isop = False
                s.isvoice = False
                s.isbanned = False
            return s

    def call(self, func, origin, bot, trigger):
        nick = trigger.nick
        if nick not in self.times:
            self.times[nick] = dict()
        if func in self.times[nick] and not trigger.admin:
            timediff = time.time() - self.times[nick][func]
            if timediff < func.rate:
                self.times[nick][func] = time.time()
                self.debug(
                    'bot.py',
                    "%s prevented from using %s in %s: %d < %d" % (
                        trigger.nick, func.__name__, trigger.sender, timediff, func.rate),
                    "warning")
                return

        try:
            exit_code = func(bot, trigger)
        except BotException:
            exit_code = None
            self.error(origin, trigger)

        if exit_code != irc.NOLIMIT:
            self.times[nick][func] = time.time()

    def limit(self, origin, func):
        return False

    def dispatch(self, origin, text, args):
        event, args = args[0], args[1:]
        wrapper = self.BotWrapper(self, origin)

        for priority in ('high', 'medium', 'low'):
            items = self.commands[priority].items()

            for regexp, funcs in items:
                match = regexp.match(text)
                if not match:
                    continue
                trigger = self.Trigger(text, origin, text, match, event, args, self)
                if not trigger.registered:
                    self.debug(
                        __file__,
                        "Prevented from using %s because user %s is not registered" % (funcs, origin.hostmask),
                        "warning")
                    return

                for func in funcs:
                    if event != func.event:
                        continue
                    if self.limit(origin, func):
                        continue
                    if func.thread:
                        targs = (func, origin, wrapper, trigger)
                        t = threading.Thread(target=self.call, args=targs)
                        t.start()
                    else:
                        self.call(func, origin, wrapper, trigger)

    def debug(self, tag, text, level):
        debug_msg = "[%s] %s" % (tag, text)
        print debug_msg 
        self.msg('stdio', debug_msg)
        return True

if __name__ == '__main__':
    print __doc__
