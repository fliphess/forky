import os
import socket
from control.bot.log import logger
from frontend.exceptions import SocketListenerError
from socket_handler.decrypt import DeCryptInput, DeCryptException


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
                d = DeCryptInput(data=input_data)
                data = d.decrypt()
                self.log.info('[SOCKET LISTENER]: %s' % data)
            except DeCryptException as e:
                self.log.info('Error decrypting incoming data from %s: %s' % (self.socket_file, e))
                continue

            if data.startswith("QUIT"):
                self.log.info('[SOCKET LISTENER] Remotely closed the listener thread')
                self.close()
                raise SocketListenerError('Socket was closed by user')
            yield data
