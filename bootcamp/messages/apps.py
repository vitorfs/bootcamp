from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MessagesConfig(AppConfig):
    name = 'bootcamp.messages'
    verbose_name = _('Messages')
