from django.db import models
from django.utils.translation import ugettext_lazy as _


class IRCMessage(models.Model):
    nick = models.CharField(_("Nickname"), max_length=100)
    message = models.TextField(_("Message"))
    channel = models.CharField(_("Channel"), max_length=100)
    message_time = models.DateTimeField(_("Time"), auto_now_add=True)

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


class IrcEvent(models.Model):
    # TODO - Log all events -> join, part, ban, kick, disconnect, topic,
    pass

class SocketEvent(models.Model):
    # TODO - Log all incoming socket events to database, except the incorrect tries to avoid flood
    pass
