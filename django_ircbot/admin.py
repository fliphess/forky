from django.contrib import admin
from django_ircbot.models import BotUser, InfoItem, Channel, Module


class BaseAdmin(admin.ModelAdmin):
    pass


@admin.register(BotUser)
class BotUserAdmin(BaseAdmin):
    fields = ('nick', 'admin', 'name', 'email', 'host', 'about', 'banned', 'operator', 'voice', 'registration_token')
    list_display = fields


@admin.register(InfoItem)
class InfoItemAdmin(BaseAdmin):
    fields = ('item', 'text')
    list_display = fields


@admin.register(Channel)
class ChannelAdmin(BaseAdmin):
    fields = ('channel', 'topic', 'key')
    list_display = fields


@admin.register(Module)
class ModuleAdmin(BaseAdmin):
    fields = ('name', 'enabled', 'filename')
    list_display = fields
