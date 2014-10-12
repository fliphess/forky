from django.contrib import admin
from frontend.models import InfoItem, Channel, Module, BotUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


class BaseAdmin(admin.ModelAdmin):
    pass


@admin.register(BotUser)
class BotUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('IRC Info'), {'fields': ('nick', 'host', 'about')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('OTP Token'), {'fields': ('registration_token',)}),
        (_('IRC Perms'), {'fields': ('is_banned', 'is_voice', 'is_operator')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('registration_token', 'email')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_banned')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


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
