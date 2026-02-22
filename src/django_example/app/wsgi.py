"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from dishka import make_container
from django.core.wsgi import get_wsgi_application

from django_example.app.ioc import AppProvider
from dmr_dishka.integration import setup_dishka

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_example.app.settings")

container = make_container(AppProvider())
setup_dishka(container)

application = get_wsgi_application()
