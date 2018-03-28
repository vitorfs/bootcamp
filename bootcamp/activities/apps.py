from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ActivitiesConfig(AppConfig):
    name = 'bootcamp.activities'
    verbose_name = _('Activities')
