from SimpleAES import SimpleAES, DecryptionError
from frontend.models import SocketUser


class DeCryptException(Exception):
    pass


class AuthDecrypt(object):
    def __init__(self, data, user):
        self.data = data
        self.token = self.verify_user(username=user)

    @staticmethod
    def verify_user(username):
        sock_user = SocketUser.objects.get(user__username=username, is_active=True)
        if not sock_user:
            raise DeCryptException('No token found in db')
        return sock_user.token

    def decrypt(self):
        try:
            a = SimpleAES(self.token)
            return a.decrypt(self.data)
        except DecryptionError as e:
            raise DeCryptException(e)
