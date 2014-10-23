class SocketException(Exception):
    pass


class SocketListenerError(SocketException):
    pass


class SocketSenderError(SocketException):
    pass