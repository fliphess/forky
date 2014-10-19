from base64 import b64decode
import os
import socket

from control.bot.log import logger
from frontend.exceptions import SocketListenerError
from control.socket_handler.decrypt import AuthDecrypt, DeCryptException


class SocketServer(object):
    def __init__(self, unix_socket='/var/run/socket_listener.sock'):
        self.socket_file = unix_socket
        self.log = logger()
        self.socket = None

    def bind(self):
        """ Server side bind() is used to bind to a socket
        """
        if os.path.exists(self.socket_file):
            os.remove(self.socket_file)
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.socket.bind(self.socket_file)
        except socket.error as e:
            raise SocketListenerError('An error appeared binding to socket %s: %s' % (self.socket_file, e))
        return True

    def close(self):
        """ Close the existing socket connection and cleanup
        """
        return self.socket.close()

    def receive(self):
        while True:
            input_data = self.socket.recv(1024)
            if not input_data:
                continue

            try:
                user, string = b64decode(input_data).split(':')
            except (ValueError, TypeError):
                self.log.warn('Bad data! Failed to get user and input data from b64 string')
                continue

            try:
                d = AuthDecrypt(data=string, user=user)
                data = d.decrypt()
                self.log.info('[SOCKET LISTENER] %s: %s' % (user, data))
            except DeCryptException as e:
                self.log.info('Error decrypting incoming data from %s: %s' % (user, e))
                continue
            yield data
