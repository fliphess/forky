from django.db import models
from django.utils.translation import ugettext_lazy as _


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


class IRCMessage(models.Model):
    nickname = models.CharField(_("Nickname"), max_length=100)
    message = models.TextField(_("Message"))
    server = models.CharField(_("Server"), max_length=100)
    channel = models.CharField(_("Channel"), max_length=100)
    message_time = models.DateTimeField(_("Time"), auto_now_add=True)
    join_or_leave = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("message_time",)

    def __unicode__(self):
        return "[%s] %s%s %s: %s" % (
            self.message_time, self.server, self.channel, self.nickname, self.short_message())

    def short_message(self):
        return self.message[:50]
    short_message.short_description = _("Message")

