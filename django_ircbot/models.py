from django.db import models


class BotUser(models.Model):
    nick = models.CharField('nick', max_length=100, unique=True)
    name = models.CharField('name', max_length=100)
    email = models.EmailField('email')

    host = models.CharField('host', max_length=100)
    about = models.TextField('about')

    banned = models.BooleanField('banned', default=False)
    registration_token = models.CharField('token', max_length=255, unique=True)

    voice = models.BooleanField('voice', default=False)
    operator = models.BooleanField('operator', default=False)
    admin = models.BooleanField('admin', default=False)


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
