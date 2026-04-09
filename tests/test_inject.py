"""
Tests for the inject / inject_sync decorators.

These tests do not use the django_example app at all.  They build a minimal
Django request by hand, attach a child container to request.META, and call
decorated functions directly — no URL routing, no views, no database.
"""

from typing import cast

import pytest
from dishka import (
    FromDishka,
    Provider,
    Scope,
    make_async_container,
    make_container,
    provide,
)
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory

from dmr_dishka.container import AsyncGetResponseCallable, container_middleware
from dmr_dishka.integration import inject, inject_sync, setup_dishka

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class GreetingProvider(Provider):
    @provide(scope=Scope.SESSION)
    def provide_greeting(self) -> str:
        return "injected_value"


class CounterProvider(Provider):
    @provide(scope=Scope.SESSION)
    def provide_int(self) -> int:
        return 42


def _make_request_with_container(container_session) -> HttpRequest:
    """Return a GET request that already has a child container in META."""
    factory = RequestFactory()
    request = factory.get("/")
    request.META["dishka_container"] = container_session
    return request


# ---------------------------------------------------------------------------
# inject (async)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_inject_resolves_dependency_from_request_container() -> None:
    """inject must pull a dependency from the container stored in request.META."""
    container = make_async_container(GreetingProvider())
    async with container(scope=Scope.SESSION) as child:
        request = _make_request_with_container(child)

        @inject
        async def handler(
            request: HttpRequest,
            greeting: FromDishka[str],
        ) -> str:
            return greeting

        result = await handler(request)
    assert result == "injected_value"


@pytest.mark.asyncio
async def test_inject_resolves_multiple_dependencies() -> None:
    """inject must handle multiple injected dependencies at once."""
    container = make_async_container(GreetingProvider(), CounterProvider())
    async with container(scope=Scope.SESSION) as child:
        request = _make_request_with_container(child)

        @inject
        async def handler(
            request: HttpRequest,
            greeting: FromDishka[str],
            count: FromDishka[int],
        ) -> tuple[str, int]:
            return greeting, count

        result = await handler(request)
    assert result == ("injected_value", 42)


@pytest.mark.asyncio
async def test_inject_passes_explicit_args_through() -> None:
    """Explicitly provided arguments must not be overridden by inject."""
    container = make_async_container(GreetingProvider())
    async with container(scope=Scope.SESSION) as child:
        request = _make_request_with_container(child)

        @inject
        async def handler(
            request: HttpRequest,
            name: str,
            greeting: FromDishka[str],
        ) -> str:
            return f"{name}:{greeting}"

        result = await handler(request, "alice")
    assert result == "alice:injected_value"


# ---------------------------------------------------------------------------
# inject_sync
# ---------------------------------------------------------------------------


def test_inject_sync_resolves_dependency_from_request_container() -> None:
    """inject_sync must pull a dependency from the container in request.META."""
    container = make_container(GreetingProvider())
    with container(scope=Scope.SESSION) as child:
        request = _make_request_with_container(child)

        @inject_sync
        def handler(request: HttpRequest, greeting: FromDishka[str]) -> str:
            return greeting

        result = handler(request)
    assert result == "injected_value"


def test_inject_sync_resolves_multiple_dependencies() -> None:
    """inject_sync must handle multiple injected dependencies."""
    container = make_container(GreetingProvider(), CounterProvider())
    with container(scope=Scope.SESSION) as child:
        request = _make_request_with_container(child)

        @inject_sync
        def handler(
            request: HttpRequest,
            greeting: FromDishka[str],
            count: FromDishka[int],
        ) -> tuple[str, int]:
            return greeting, count

        result = handler(request)
    assert result == ("injected_value", 42)


# ---------------------------------------------------------------------------
# inject via middleware (end-to-end without example app)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_inject_via_middleware_full_cycle() -> None:
    """
    Full cycle: middleware attaches container → inject resolves dependency.
    No django_example app involved.
    """
    from django.conf import settings as django_settings

    original_container = getattr(django_settings, "__DISHKA_CONTAINER__", None)
    container = make_async_container(GreetingProvider())
    setup_dishka(container)
    try:
        resolved: dict[str, object] = {}

        @inject
        async def get_response(
            request: HttpRequest,
            greeting: FromDishka[str],
        ) -> HttpResponse:
            resolved["greeting"] = greeting
            return HttpResponse("ok")

        middleware = cast(
            AsyncGetResponseCallable,
            container_middleware(get_response),
        )
        factory = RequestFactory()
        response = await middleware(factory.get("/"))

        assert response.status_code == 200
        assert resolved["greeting"] == "injected_value"
    finally:
        if original_container is not None:
            django_settings.__DISHKA_CONTAINER__ = original_container
