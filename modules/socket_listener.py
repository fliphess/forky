from django.conf import settings
from control.bot.decorators import event, priority, thread, rule

from control.socket_handler.server import SocketServer


@event('251')
@rule('.*')
@priority('high')
@thread(True)
def socket_server(bot, trigger):
    """
    Runs when we recived 251 - lusers, which is just before the server sends the motd,
    and right after establishing a sucessful connection.
    """
    p = SocketServer(unix_socket=settings.LISTENER_SOCKET)
    p.bind()
    for incoming in p.receive():
        if not incoming:
            continue
        bot.write(incoming.split())
