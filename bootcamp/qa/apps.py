from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class QaConfig(AppConfig):
    name = 'bootcamp.qa'
    verbose_name = _('Q&A')
