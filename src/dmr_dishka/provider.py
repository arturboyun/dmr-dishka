from dishka import Provider, Scope, from_context
from django.http import HttpRequest


class DjangoProvider(Provider):
    request = from_context(HttpRequest, scope=Scope.SESSION)
