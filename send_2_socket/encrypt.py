from base64 import b64encode
from SimpleAES import SimpleAES


class EnCryptException(Exception):
    pass


class EnCryptInput(object):
    def __init__(self, string, user):
        self.user = user
        self.string = string

    def encrypt(self, token):
        return b64encode('%s:%s' % (self.user, self._encrypt(self.string, token)))

    @staticmethod
    def _encrypt(string, token):
        aes = SimpleAES(token)
        try:
            return aes.encrypt(string)
        except (ValueError, TypeError) as e:
            raise EnCryptException('Smelly data input: %s' % e)