from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from archer_apps.utils.types import ChoicesEnum


class StatusTypes(ChoicesEnum):
    UNREVIEWED = 'Unreviewed'
    REVIEWED = 'Reviewed'


class Article(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False, null=True)
    content = models.TextField(_('content'), null=True, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('creator'),
                                related_name='creator')
    status = models.CharField(_('status'), max_length=16, choices=StatusTypes.choices())
    created = models.DateField(_('created'), auto_now_add=True)

    def __str__(self):
        return f'{self.title}'
