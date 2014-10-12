# coding=utf-8
import signal
import sys
import os
import re
import threading

try:
    import ssl
    import OpenSSL
except ImportError:
    ssl = False
import Queue
import copy


class Watcher(object):
    def __init__(self):
        self.child = os.fork()
        if self.child != 0:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError:
            pass


def get_command_regexp(prefix, command):
    # This regexp match equivalently and produce the same
    # groups 1 and 2 as the old regexp: r'^%s(%s)(?: +(.*))?$'
    # The only differences should be handling all whitespace
    # like spaces and the addition of groups 3-6.
    #
    # Regex:
    #
    #     {prefix}({command}) # Command as group 1.
    #     (?:\s+              # Whitespace to end command.
    #     (                   # Rest of the line as group 2.
    #     (?:(\S+))?          # Parameters 1-4 as groups 3-6.
    #     (?:\s+(\S+))?
    #     (?:\s+(\S+))?
    #     (?:\s+(\S+))?
    #     .*                  # Accept anything after the parameters. Leave it up to the module to parse the line.
    #     ))?                 # Group 2 must be None, if there are no parameters.
    #     $                   # EoL, so there are no partial matches.
    pattern = r"""{prefix}({command})(?:\s+((?:(\S+))?(?:\s+(\S+))?(?:\s+(\S+))?(?:\s+(\S+))?.*))?$""".format(
        prefix=prefix,
        command=command)
    return re.compile(pattern, re.IGNORECASE | re.VERBOSE)


class PriorityQueue(Queue.PriorityQueue):
    """ A priority queue with a peek method. """

    def peek(self):
        """ Return a copy of the first element without removing it. """
        self.not_empty.acquire()
        try:
            while not self._qsize():
                self.not_empty.wait()
            # Return a copy to avoid corrupting the heap. This is important
            # for thread safety if the object is mutable.
            return copy.deepcopy(self.queue[0])
        finally:
            self.not_empty.release()


class Released(object):
    """ A context manager that releases a lock temporarily. """
    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        self.lock.release()

    def __exit__(self, _type, _value, _traceback):
        self.lock.acquire()


class Nick(unicode):
    def __new__(cls, nick):
        s = unicode.__new__(cls, nick)
        s._lowered = Nick._lower(nick)
        return s

    def lower(self):
        return self._lowered

    @staticmethod
    def _lower(nick):
        low = nick.lower().replace('{', '[').replace('}', ']')
        low = low.replace('|', '\\').replace('^', '~')
        return low


def verify_ssl_cn(server, port):
    """
    *Availability: Must have the OpenSSL Python module installed.*

    Verify the SSL certificate given by the ``server`` when connecting on the
    given ``port``. This returns ``None`` if OpenSSL is not available or
    'NoCertFound' if there was no certificate given. Otherwise, a two-tuple
    containing a boolean of whether the certificate is valid and the
    certificate information is returned.
    """
    if not ssl:
        return None
    cert = None
    for version in (ssl.PROTOCOL_TLSv1, ssl.PROTOCOL_SSLv3, ssl.PROTOCOL_SSLv23):
        try:
            cert = ssl.get_server_certificate((server, port), ssl_version=version)
            break
        except Exception as e:
            pass
    if cert is None:
        return 'NoCertFound'
    valid = False

    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    cert_info = x509.get_subject().get_components()
    cn = x509.get_subject().commonName
    if cn == server:
        valid = True
    elif '*' in cn:
        cn = cn.replace('*.', '')
        if re.match('(.*)%s' % cn, server, re.IGNORECASE) is not None:
            valid = True
    return valid, cert_info


class BotMemory(dict):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BotMemory, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args):
        super(BotMemory, self).__init__(self, *args)
        self.lock = threading.Lock()

    def __setitem__(self, key, value):
        self.lock.acquire()
        result = dict.__setitem__(self, key, value)
        self.lock.release()
        return result

    def __contains__(self, key):
        """ Check if a key is in the dict, locking it for writes when doing so. """
        self.lock.acquire()
        result = dict.__contains__(self, key)
        self.lock.release()
        return result

    def contains(self, key):
        """ Backwards compatibility with 3.x, use `in` operator instead """
        return self.__contains__(key)

    def lock(self):
        """ Lock this instance from writes. Useful if you want to iterate """
        return self.lock.acquire()

    def unlock(self):
        """ Release the write lock """
        return self.lock.release()
