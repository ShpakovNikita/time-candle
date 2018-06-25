"""
WSGI config for time_candle project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
from main_system import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "time_candle.settings")

application = get_wsgi_application()
if not settings.DEBUG:
    application = DjangoWhiteNoise(application)
