"""
Unit tests for dmr_dishka.container.container_middleware.

These tests exercise the middleware in isolation without hitting Django's
full URL routing stack.  The session-scoped `setup_test_container` fixture
in conftest.py wires an async Container into Django settings before any of
these tests run.
"""

from typing import cast

from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory

from dmr_dishka.container import AsyncGetResponseCallable, container_middleware

# ---------------------------------------------------------------------------
# Async middleware
# ---------------------------------------------------------------------------


async def test_async_middleware_attaches_container() -> None:
    """The middleware must put a child container in request.META."""
    factory = RequestFactory()
    request = factory.get("/")

    async def get_response(req: HttpRequest) -> HttpResponse:
        assert "dishka_container" in req.META, (
            "container_middleware did not set request.META['dishka_container']"
        )
        return HttpResponse("ok")

    middleware = cast(
        AsyncGetResponseCallable,
        container_middleware(get_response),
    )
    response = await middleware(request)
    assert response.status_code == 200


async def test_async_middleware_container_resolves_dependency() -> None:
    """The child container attached to the request must resolve providers."""
    factory = RequestFactory()
    request = factory.get("/")
    resolved: dict[str, object] = {}

    async def get_response(req: HttpRequest) -> HttpResponse:
        child = req.META["dishka_container"]
        resolved["value"] = await child.get(str)
        return HttpResponse("ok")

    middleware = cast(
        AsyncGetResponseCallable,
        container_middleware(get_response),
    )
    await middleware(request)

    assert resolved["value"] == "Hello from Dishka!"


async def test_async_middleware_container_is_scoped_per_request() -> None:
    """Each call to the middleware must produce a fresh child container."""
    factory = RequestFactory()
    containers = []

    async def get_response(req: HttpRequest) -> HttpResponse:
        containers.append(req.META["dishka_container"])
        return HttpResponse("ok")

    middleware = cast(
        AsyncGetResponseCallable,
        container_middleware(get_response),
    )
    await middleware(factory.get("/"))
    await middleware(factory.get("/"))

    assert containers[0] is not containers[1], (
        "Expected a new child container per request"
    )
