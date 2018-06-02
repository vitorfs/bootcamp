from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'bootcamp.users'
    verbose_name = _("Users")

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        try:
            import users.signals  # noqa F401

        except ImportError:
            pass
