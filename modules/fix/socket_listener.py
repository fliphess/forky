import os
import socket
from control.bot.log import logger


class SocketListenerError(StandardError):
    pass


class SocketListener(object):
    def __init__(self, unix_socket='/var/run/socket_listener.sock', pidfile='/var/run/socket_listener.pid'):
        self.socket = unix_socket
        self.pid_file = pidfile
        self.log = logger()
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    def connect(self):
        if os.path.isfile(self.pid_file):
            raise SocketListenerError('Pidfile %s allready in place! Please kill other instance first' % self.pid_file)
        if os.path.exists(self.socket):
            os.remove(self.socket)
        try:
            self.server.bind(self.socket)
        except socket.error as e:
            raise SocketListenerError('An error appeared binding to socket %s: %s' % (self.socket, e))
        return True

    def close(self):
        self.server.close()
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

    def receive(self):
        while True:
            datagram = self.server.recv(1024)
            if not datagram:
                continue

            self.log.info('[SOCKET LISTENER] Socket input: %s' % datagram)
            if datagram.startswith("QUIT"):
                self.log.info('[SOCKET LISTENER] Remotely closed the listener thread')
                self.close()
                break
            yield datagram


