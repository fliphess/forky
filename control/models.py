from django.db import models


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