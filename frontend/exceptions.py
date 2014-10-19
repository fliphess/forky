class BotException(Exception):
    pass


class SocketException(Exception):
    pass


class SocketSenderError(SocketException):
    pass


class SocketListenerError(SocketException):
    pass