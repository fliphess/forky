from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from control.admin import BaseAdmin
from profile.models import SocketUser, BotUser


admin.site.unregister(Group)


@admin.register(SocketUser)
class SocketUserAdmin(BaseAdmin):
    fields = ('user', 'token', 'is_active')
    readonly_fields = ('token',)
    list_display = fields


@admin.register(BotUser)
class BotUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('IRC Info'), {'fields': ('nick', 'host', 'about')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('OTP Token'), {'fields': ('registration_token',)}),
        (_('IRC Perms'), {'fields': ('registered', 'is_login', 'is_banned', 'is_voice', 'is_operator')}),
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
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_banned', 'is_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)