from django.conf import settings
from django.db import models
from django.utils import timezone


class Quote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    quote = models.TextField('quote')
    date_added = models.DateTimeField('date_added', default=timezone.now)

    class Meta:
        unique_together = ('user', 'quote',)


class InfoItem(models.Model):
    item = models.CharField('item', max_length=100, unique=True)
    text = models.TextField('text')