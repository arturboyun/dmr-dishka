"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from dishka import make_async_container
from django.core.asgi import get_asgi_application

from django_example.app.ioc import AppProvider
from dmr_dishka.integration import setup_dishka

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_example.app.settings")

container = make_async_container(AppProvider())
setup_dishka(container)

application = get_asgi_application()
