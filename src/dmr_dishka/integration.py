import logging
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar, cast

from dishka import AsyncContainer, Container
from dishka.integrations.base import wrap_injection
from django.conf import settings
from django.http import HttpRequest

T = TypeVar("T")
P = ParamSpec("P")


logger = logging.getLogger(__name__)


def container_getter_sync(
    args: tuple[Any, ...],
    _: dict[str, Any],
) -> Container:
    if isinstance(args[0], HttpRequest):
        return cast(Container, args[0].META["dishka_container"])
    return cast(Container, args[0].request.META["dishka_container"])


def container_getter_async(
    args: tuple[Any, ...],
    _: dict[str, Any],
) -> AsyncContainer:
    if isinstance(args[0], HttpRequest):
        return cast(AsyncContainer, args[0].META["dishka_container"])
    return cast(AsyncContainer, args[0].request.META["dishka_container"])


def inject(func: Callable[P, T]) -> Callable[P, T]:
    return wrap_injection(
        func=func,
        is_async=True,
        manage_scope=True,
        container_getter=container_getter_async,
    )


def inject_sync(func: Callable[P, T]) -> Callable[P, T]:
    return wrap_injection(
        func=func,
        is_async=False,
        manage_scope=True,
        container_getter=container_getter_sync,
    )


def setup_dishka(container: AsyncContainer | Container) -> None:
    if "dmr_dishka.container.container_middleware" not in settings.MIDDLEWARE:
        settings.MIDDLEWARE.append("dmr_dishka.container.container_middleware")
    settings.__DISHKA_CONTAINER__ = container
