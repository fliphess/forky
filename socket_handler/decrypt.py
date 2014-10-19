from base64 import b64decode
from SimpleAES import SimpleAES, DecryptionError
from frontend.models import SocketUser


class DeCryptException(Exception):
    pass


class DeCryptInput(object):
    def __init__(self, data):
        self.user, self.string = self.prepare(data)
        self.token = self.get_token(self.user)

    @staticmethod
    def prepare(data):
        try:
            return b64decode(data).split(':')
        except (ValueError, TypeError):
            raise DeCryptException('Bad data! Failed to get user and input data from b64 string')

    @staticmethod
    def get_token(username):
        sock_user = SocketUser.objects.get(user__username=username, is_active=True)
        if not sock_user:
            raise DeCryptException('No token found for user')
        return sock_user.token

    def decrypt(self):
        try:
            a = SimpleAES(self.token)
            return a.decrypt(self.string)
        except DecryptionError as e:
            raise DeCryptException(e)
