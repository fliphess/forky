import json
from django.conf import settings
from socket_handler import SocketHandler


def setup(bot):
    pass

def socket_server():
    p = SocketHandler(pidfile=settings.LISTENER_PID, unix_socket=settings.LISTENER_SOCKET)
    p.bind()
    for incoming in p.receive():
        if not incoming:
            continue
        try:
            data = json.loads(incoming)
        except (ValueError, TypeError) as e:
            p.log.error('Failed to parse input: %s' % e)
            continue
        # Check if token is present

        # Get token user

        # Check user status

        # If user status

        # Send to server