from base64 import b64decode
import os
import socket
from SimpleAES import SimpleAES
from control.bot.log import logger
from frontend.models import SocketUser


class SocketException(Exception):
    pass


class SocketListenerError(SocketException):
    pass


class SocketSenderError(SocketException):
    pass


class SocketHandler(object):
    def __init__(self, unix_socket='/var/run/socket_listener.sock', pidfile='/var/run/socket_listener.pid'):
        self.socket_file = unix_socket
        self.pid_file = pidfile
        self.log = logger()
        self.socket = None

    def bind(self):
        """ Server side bind() is used to bind to a socket
        """
        if os.path.exists(self.pid_file):
            raise SocketListenerError('Pidfile %s already in place! Please kill other instance first' % self.pid_file)

        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.socket.bind(self.socket_file)
        except socket.error as e:
            raise SocketListenerError('An error appeared binding to socket %s: %s' % (self.socket_file, e))
        return True

    def connect(self):
        """ Clients use connect to connect to an existing socket
        """
        if not os.path.exists(self.socket_file):
            raise SocketListenerError('Socket %s not found!' % self.socket_file)
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.socket.connect(self.socket_file)
        except socket.error as e:
            raise SocketListenerError('An error appeared binding to socket %s: %s' % (self.socket_file, e))
        return True

    def close(self):
        """ Close the existing socket connection and cleanup
        """
        return self.socket.close()

    def receive(self):
        while True:
            datagram = self.socket.recv(1024)
            if not datagram:
                continue
            self.log.info('[SOCKET LISTENER]: %s' % datagram)
            if datagram.startswith("QUIT"):


                self.log.info('[SOCKET LISTENER] Remotely closed the listener thread')
                self.close()
                break
            yield datagram

    def send(self, data):
        try:
            self.socket.send(data)
        except socket.error as e:
            raise SocketSenderError('Failed to send to socket %s' % self.socket_file)
        return True


class SocketInput(object):
    def __init__(self, token, data):
        self.aes = SimpleAES(token)
        self.data = data

    def decrypt(self):
        user, string = self.split_data(data)
        return self.aes.decrypt(data)

    def encrypt(self, data):
        return self.aes.decrypt(data)

    @staticmethod
    def split_data(data):
        try:
            username, string = b64decode(data).split(':')
            return username, string
        except (ValueError, TypeError):
            raise SocketException('Smelly data input!')

    @staticmethod
    def get_token(username):
        tokens = SocketUser.objects.filter(user=username, active=True)
        if not tokens:
            return False
        return tokens[0]
