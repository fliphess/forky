import sys
import time
import socket
import asyncore
import asynchat
import codecs
import traceback
from django.conf import settings
import re
from control.bot.log import logger
from tools import Nick

try:
    import select
    import ssl
    has_ssl = True
except:
    has_ssl = False

import errno
import threading
from datetime import datetime
from tools import verify_ssl_cn


NOLIMIT = 1
VOICE = 1
HALFOP = 2
OP = 4
ADMIN = 8
OWNER = 16


class Origin(object):
    source = re.compile(r'([^!]*)!?([^@]*)@?(.*)')

    def __init__(self, bot, source, args):
        self.hostmask = source

        match = Origin.source.match(source or '')
        self.nick, self.user, self.host = match.groups()
        self.nick = Nick(self.nick)

        if len(args) > 1:
            target = args[1]
        else:
            target = None
        if target and target.lower() == bot.nick.lower():
            target = self.nick
        self.sender = target


class Bot(asynchat.async_chat):
    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.set_terminator('\n')
        self.error_count = 0
        self.last_error_timestamp = datetime.now()
        self.buffer = ''

        self.nick = Nick(settings.BOT_NICK)
        self.ident = settings.BOT_IDENT
        self.name = settings.BOT_NAME
        self.log = logger()

        self.stack = []
        self.channels = []
        self.ca_certs = '/etc/pki/tls/cert.pem'
        self.has_quit = False

        self.sending = threading.RLock()
        self.writing_lock = threading.Lock()

        self.last_ping_time = None
        self.raw = None
        self.ssl = None

    def safe(self, string):
        string = string.replace('\n', '')
        string = string.replace('\r', '')
        if not isinstance(string, unicode):
            string = unicode(string, encoding='utf8')
        return string

    def write(self, args, text=None):
        args = [self.safe(arg) for arg in args]
        if text is not None:
            text = self.safe(text)
        try:
            self.writing_lock.acquire()
            if text is not None:
                temp = (u' '.join(args) + ' :' + text)[:510] + '\r\n'
            else:
                temp = u' '.join(args)[:510] + '\r\n'
            self.send(temp.encode('utf-8'))

            self.log.debug(temp.encode('utf-8'))
        finally:
            self.writing_lock.release()

    def run(self, host, port=6667):
        self.initiate_connect(host, port)

    def initiate_connect(self, host, port):
        self.log.info('Connecting to %s:%s...' % (host, port))

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        if settings.IRC_SERVER_SSL and has_ssl:
            self.send = self._ssl_send
            self.recv = self._ssl_recv
        elif not has_ssl and settings.IRC_SERVER_SSL:
            self.log.error('SSL is not available on your system, attempting connection without it')

        self.connect((host, port))
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            self.log.error('KeyboardInterrupt')
            self.quit('KeyboardInterrupt')

    def quit(self, message):
        """ Disconnect from IRC and close the bot"""
        self.write(['QUIT'], message)
        self.has_quit = True
        self.handle_close()

    def part(self, channel, msg=None):
        """ Part a channel"""
        self.write(['PART', channel], msg)

    def join(self, channel, password=None):
        """ Join a channel"""
        if password is None:
            self.write(['JOIN'], channel)
        else:
            self.write(['JOIN', channel, password])

    def handle_connect(self):
        if settings.IRC_SERVER_SSL and has_ssl:
            if not settings.IRC_SERVER_VERIFY_SSL:
                self.ssl = ssl.wrap_socket(self.socket, do_handshake_on_connect=False, suppress_ragged_eofs=True)
            else:
                verification = verify_ssl_cn(settings.IRC_SERVER_HOST, int(settings.IRC_SERVER_PORT))

                if verification is 'NoCertFound':
                    self.log.error("Can't get server certificate, SSL might be disabled on the server.")
                    sys.exit(1)
                elif verification is not None:
                    self.log.error('\nSSL Cert information: %s' % verification[1])
                    if verification[0] is False:
                        self.log.error("Invalid certificate, CN mismatch!")
                        sys.exit(1)
                else:
                    self.log.error('WARNING! certificate information and CN validation are not available. '
                                   'Is pyOpenSSL installed?')
                    self.log.error('Trying to connect anyway:')
                self.ssl = ssl.wrap_socket(
                    self.socket,
                    do_handshake_on_connect=False,
                    suppress_ragged_eofs=True,
                    cert_reqs=ssl.CERT_REQUIRED,
                    ca_certs=self.ca_certs)

            self.log.info('\nSSL Handshake intiated...')
            error_count = 0
            while True:
                try:
                    self.ssl.do_handshake()
                    break
                except ssl.SSLError, err:
                    if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                        select.select([self.ssl], [], [])
                    elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                        select.select([], [self.ssl], [])
                    elif err.args[0] == 1:
                        self.log.error('SSL Handshake failed with error: %s' % err.args[1])
                        sys.exit(1)
                    else:
                        error_count += 1
                        if error_count > 5:
                            self.log.error('SSL Handshake failed (%d failed attempts)' % error_count)
                            sys.exit(1)
                        raise
                except Exception as e:
                    self.log.error('SSL Handshake failed with error: %s' % e)
                    sys.exit(1)
            self.set_socket(self.ssl)

        if settings.IRC_SERVER_PASSWORD is not None:
            self.write(('PASS', settings.IRC_SERVER_PASSWORD))
        self.write(('NICK', self.nick))
        self.write(('USER', self.ident, '+iw', self.nick), self.name)

        self.log.info('Connected.')
        self.last_ping_time = datetime.now()
        timeout_check_thread = threading.Thread(target=self._timeout_check)
        timeout_check_thread.start()
        ping_thread = threading.Thread(target=self._send_ping)
        ping_thread.start()

    def _timeout_check(self):
        while True:
            if (datetime.now() - self.last_ping_time).seconds > int(settings.IRC_SERVER_TIMEOUT):
                self.log.error(
                    'Ping timeout reached after %s seconds, closing connection' % settings.IRC_SERVER_TIMEOUT)
                self.handle_close()
                break
            else:
                time.sleep(int(settings.IRC_SERVER_TIMEOUT))

    def _send_ping(self):
        while True:
            if (datetime.now() - self.last_ping_time).seconds > int(settings.IRC_SERVER_TIMEOUT) / 2:
                self.write(('PING', settings.IRC_SERVER_HOST))
            time.sleep(int(settings.IRC_SERVER_TIMEOUT / 2))

    def _ssl_send(self, data):
        """ Replacement for self.send() during SSL connections. """
        try:
            result = self.socket.send(data)
            return result
        except ssl.SSLError, why:
            if why[0] in (asyncore.EWOULDBLOCK, errno.ESRCH):
                return 0
            else:
                raise ssl.SSLError, why

    def _ssl_recv(self, buffer_size):
        """ Replacement for self.recv() during SSL connections. From:
            http://evanfosmark.com/2010/09/ssl-support-in-asynchatasync_chat
        """
        try:
            data = self.socket.read(buffer_size)
            if not data:
                self.handle_close()
                return ''
            return data
        except ssl.SSLError, why:
            if why[0] in (asyncore.ECONNRESET, asyncore.ENOTCONN,
                          asyncore.ESHUTDOWN):
                self.handle_close()
                return ''
            elif why[0] == errno.ENOENT:
                return ''
            else:
                raise

    def handle_close(self):
        self.close()
        self.log.info('Closed!')

    def collect_incoming_data(self, data):
        try:
            data = unicode(data, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                data = unicode(data, encoding='cp1252')
            except UnicodeDecodeError:
                try:
                    data = unicode(data, encoding='iso8859-1')
                except:
                    return
        self.buffer += data

    def found_terminator(self):
        line = self.buffer

        if line:
            self.log.debug(line)

        if line.endswith('\r'):
            line = line[:-1]
        self.buffer = u''
        self.raw = line

        if line.startswith(':'):
            source, line = line[1:].split(' ', 1)
        else:
            source = None

        if ' :' in line:
            argstr, text = line.split(' :', 1)
            args = argstr.split()
            args.append(text)
        else:
            args = line.split()
            text = args[-1]

        self.last_ping_time = datetime.now()
        if args[0] == 'PING':
            self.write(('PONG', text))
        elif args[0] == 'ERROR':
            self.log.warn('IRC Server Error: %s' % text)
        elif args[0] == '433':
            self.log.error('Nickname already in use!')
            self.has_quit = True
            self.handle_close()
        origin = Origin(self, source, args)
        self.dispatch(origin, text, args)

    def dispatch(self, origin, text, args):
        pass

    def msg(self, recipient, text, max_messages=1):
        # We're arbitrarily saying that the max is 400 bytes of text when
        # messages will be split. Otherwise, we'd have to account for the bot's hostmask, which is hard.
        max_text_length = 400
        encoded_text = text.encode('utf-8')
        excess = ''

        if max_messages > 1 and len(encoded_text) > max_text_length:
            last_space = encoded_text.rfind(' ', 0, max_text_length)
            if last_space == -1:
                excess = encoded_text[max_text_length:]
                encoded_text = encoded_text[:max_text_length]
            else:
                excess = encoded_text[last_space + 1:]
                encoded_text = encoded_text[:last_space]
            text = encoded_text.decode('utf-8')

        try:
            self.sending.acquire()
            if self.stack:
                elapsed = time.time() - self.stack[-1][0]
                if elapsed < 3:
                    penalty = float(max(0, len(text) - 50)) / 70
                    wait = 0.8 + penalty
                    if elapsed < wait:
                        time.sleep(wait - elapsed)

            messages = [m[1] for m in self.stack[-8:]]
            if messages.count(text) >= 5:
                text = '...'
                if messages.count('...') >= 3:
                    return

            self.write(('PRIVMSG', recipient), text)
            self.stack.append((time.time(), self.safe(text)))
            self.stack = self.stack[-10:]
        finally:
            self.sending.release()

        if excess:
            self.msg(recipient, excess, max_messages - 1)

    def notice(self, dest, text):
        """ Send an IRC NOTICE to a user or a channel. See IRC protocol documentation for more information"""
        self.write(('NOTICE', dest), text)

    def error(self, origin=None, trigger=None):
        """ Called internally when a module causes an error """
        signature = ''
        try:
            trace = traceback.format_exc()
            trace = trace.decode('utf-8', errors='xmlcharrefreplace')
            self.log.error(trace)
            try:
                lines = list(reversed(trace.splitlines()))
                report = [lines[0].strip()]
                for line in lines:
                    line = line.strip()
                    if line.startswith('File "/'):
                        report.append(line[0].lower() + line[1:])
                        break
                else:
                    report.append('source unknown')
                signature = '%s (%s)' % (report[0], report[1])
                log_filename = settings.LOG_EXCEPTIONS
                with codecs.open(log_filename, 'a', encoding='utf-8') as logfile:
                    logfile.write(u'Signature: %s\n' % signature)

                    if origin:
                        logfile.write(u'from %s at %s:\n' % (origin.sender, str(datetime.now())))

                    if trigger:
                        logfile.write(u'Message was: <%s> %s\n' % (trigger.nick, trigger.group(0)))

                    logfile.write(trace)
                    logfile.write('----------------------------------------\n\n')

            except Exception as e:
                self.log.error("Could not save full traceback!")
                self.log.warn("Error reporting: (From: %s), can't save traceback: %s" % (origin.sender, str(e)))
            if origin:
                self.msg(recipient=origin.sender, text=signature)

        except Exception as e:
            if origin:
                self.msg(origin.sender, "Got an error.")
                self.log.warn("Error reporting (From: %s) %s" % (origin.sender, str(e)))

    def handle_error(self):
        """ Handle any un captured error in the core. Overrides asyncore's handle_error """
        trace = traceback.format_exc()
        self.log.error(trace)
        self.log.warn('Fatal error in core, please review exception log')

        logfile = codecs.open(settings.LOG_EXCEPTIONS, 'a', encoding='utf-8')
        logfile.write('Fatal error in core, handle_error() was called\n')
        logfile.write('last raw line was %s' % self.raw)
        logfile.write(trace)
        logfile.write('Buffer:\n')
        logfile.write(self.buffer)
        logfile.write('----------------------------------------\n\n')
        logfile.close()

        if self.error_count > 10:
            if (datetime.now() - self.last_error_timestamp).seconds < 5:
                self.log.error("Too many errors, can't continue")
                sys.exit(1)

        self.last_error_timestamp = datetime.now()
        self.error_count += 1
        if settings.BOT_EXIT_ON_ERROR:
            sys.exit(1)


if __name__ == "__main__":
    print __doc__
