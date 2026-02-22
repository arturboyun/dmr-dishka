from collections.abc import Callable
from typing import ParamSpec, TypeVar

from dishka import AsyncContainer, Container
from dishka.integrations.base import wrap_injection
from django.conf import settings

T = TypeVar("T")
P = ParamSpec("P")


def inject(func: Callable[P, T]) -> Callable[P, T]:
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=lambda r, _: r[0].request.META["dishka_container"],
    )


def inject_sync(func: Callable[P, T]) -> Callable[P, T]:
    return wrap_injection(
        func=func,
        is_async=False,
        container_getter=lambda r, _: r[0].request.META["dishka_container"],
    )


def setup_dishka(container: AsyncContainer | Container) -> None:
    if "dmr_dishka.container.container_middleware" not in settings.MIDDLEWARE:
        settings.MIDDLEWARE.append("dmr_dishka.container.container_middleware")
    settings.__DISHKA_CONTAINER__ = container
