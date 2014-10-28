from django.contrib import admin
from control.admin import BaseAdmin
from items.models import Quote, InfoItem


@admin.register(Quote)
class QuoteAdmin(BaseAdmin):
    fields = ('user', 'quote', 'date_added')
    list_display = fields


@admin.register(InfoItem)
class InfoItemAdmin(BaseAdmin):
    fields = ('item', 'text')
    list_display = fields