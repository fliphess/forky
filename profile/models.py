import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


def rand_key(size):
    return ''.join([random.choice(string.letters + string.digits) for i in range(size)])


class BotUser(AbstractUser):
    nick = models.CharField('nick', max_length=100, db_index=True, unique=True)
    host = models.CharField('host', max_length=100, default="ident@some-domain-name.com")
    about = models.TextField('about', default="unset")

    is_banned = models.BooleanField('banned', default=False)
    is_voice = models.BooleanField('voice', default=False)
    is_operator = models.BooleanField('operator', default=False)
    is_login = models.BooleanField('login', default=False)

    registration_token = models.CharField('token', max_length=255, unique=True, db_index=True)
    registered = models.BooleanField('registered', default=False)

    def renew_token(self):
        self.registration_token = None
        self.save()

    def enable_web(self):
        self.is_active = True
        self.save()

    def disable_web(self):
        self.is_active = False
        self.save()

    def login_user(self):
        self.is_login = True
        self.save()

    def logout_user(self):
        self.is_login = False
        self.save()

    def register_user(self):
        token_user, create = SocketUser.objects.get_or_create(user=user)
        token_user.is_active = True
        token_user.save()
        self.registered = True
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.nick is None or len(self.nick) == 0:
            self.nick = '%s%s_%s' % (self.first_name.title() or 'None', self.last_name.title() or 'None', rand_key(4))

        if self.registration_token is None or len(self.registration_token) == 0:
            self.registration_token = rand_key(settings.REGISTRATION_TOKEN_SIZE)
        models.Model.save(self, force_insert, force_update, using, update_fields)

    def _get_full_name(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name.title(), self.last_name.title())
        return "Anonymous chatter"
    real_name = property(_get_full_name)


class SocketUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    token = models.CharField('token', max_length=255, unique=True, db_index=True, default=None)
    is_active = models.BooleanField('active', default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.token is None or len(self.token) == 0:
            self.token = rand_key(settings.REGISTRATION_TOKEN_SIZE)
        models.Model.save(self, force_insert, force_update, using, update_fields)