from django.contrib import admin
from control.admin import BaseAdmin
from event_logging.models import IRCMessage


@admin.register(IRCMessage)
class IRCMessageAdmin(BaseAdmin):
    list_display = ("message_time", "server", "channel", "nickname", "short_message")
    list_filter = ("server", "channel", "nickname")
    search_fields = ("channel", "nickname", "message")
    date_hierarchy = "message_time"