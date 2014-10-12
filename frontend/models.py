from django.contrib.auth.models import AbstractUser
from django.db import models


class BotUser(AbstractUser):
    nick = models.CharField('nick', max_length=100, default="unset")
    host = models.CharField('host', max_length=100, default="unset")
    about = models.TextField('about', default="unset")
    is_banned = models.BooleanField('banned', default=False)
    is_voice = models.BooleanField('voice', default=False)
    is_operator = models.BooleanField('operator', default=False)
    registration_token = models.CharField('token', max_length=255, blank=True)


class InfoItem(models.Model):
    item = models.CharField('item', max_length=100, unique=True)
    text = models.TextField('text')


class Channel(models.Model):
    channel = models.CharField('channel', max_length=100, unique=True)
    topic = models.CharField('topic', max_length=255)
    key = models.CharField('key', max_length=255, blank=True)


class Module(models.Model):
    name = models.CharField('name', max_length=100, unique=True)
    enabled = models.BooleanField('enabled', default=True)
    filename = models.CharField('filename', max_length=100, unique=False)


class Ban(models.Model):
    nick = models.CharField('nick', max_length=100, unique=True)
    host = models.CharField('host', max_length=100)
