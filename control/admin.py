from django.contrib import admin

from control.models import Channel, Module, Ban


class BaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Module)
class ModuleAdmin(BaseAdmin):
    fields = ('name', 'enabled', 'filename')
    list_display = fields


@admin.register(Ban)
class BanAdmin(BaseAdmin):
    fields = ('nick', 'host')
    list_display = fields


@admin.register(Channel)
class ChannelAdmin(BaseAdmin):
    fields = ('channel', 'topic', 'key')
    list_display = fields


