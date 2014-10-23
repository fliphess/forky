import os
import socket
from control.socket_handler.exceptions import SocketListenerError, SocketSenderError

from control.socket_handler.encrypt import AuthCrypt


class SocketSender(object):
    def __init__(self, user, token, unix_socket='/var/run/socket_listener.sock'):
        self.user = user
        self.token = token
        self.socket_file = unix_socket
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    def connect(self):
        """ Clients use connect to connect to an existing socket
        """
        if not os.path.exists(self.socket_file):
            raise SocketSenderError('Socket %s not found!' % self.socket_file)
        try:
            self.socket.connect(self.socket_file)
        except socket.error as e:
            raise SocketSenderError('An error appeared binding to socket %s: %s' % (self.socket_file, e))
        return True

    def close(self):
        """ Close the existing socket connection and cleanup
        """
        return self.socket.close()

    def send(self, string):
        c = AuthCrypt(string=string, user=self.user)
        output = c.encrypt(token=self.token)
        try:
            self.socket.send(output)
        except socket.error as e:
            raise SocketSenderError('Failed to send to socket %s: %s' % (self.socket_file, e))
        return True