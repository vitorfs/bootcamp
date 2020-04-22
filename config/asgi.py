"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application

import logging

logger = logging.getLogger(__name__)
logger.debug(' ------- HELLLLLOOOOOOOOOOOOOO!!!!!!!!!!!!!!!!!!yeahhhhhhh ----------------------- !!!!!!')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()
application = get_default_application()
