from collections.abc import Awaitable, Callable
from inspect import iscoroutinefunction
from typing import cast

from dishka import Scope
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import sync_and_async_middleware

SyncGetResponseCallable = Callable[[HttpRequest], HttpResponse]
AsyncGetResponseCallable = Callable[
    [HttpRequest],
    Awaitable[HttpResponse],
]
GetResponseCallable = SyncGetResponseCallable | AsyncGetResponseCallable


@sync_and_async_middleware
def container_middleware(
    get_response: GetResponseCallable,
) -> GetResponseCallable:

    if iscoroutinefunction(get_response):
        async_get_response = cast(AsyncGetResponseCallable, get_response)

        async def async_middleware(request: HttpRequest) -> HttpResponse:
            async with settings.__DISHKA_CONTAINER__(
                {HttpRequest: request},
                scope=Scope.SESSION,
            ) as request_container:
                request.META["dishka_container"] = request_container
                return await async_get_response(request)

    else:
        get_response = cast(SyncGetResponseCallable, get_response)

        def sync_middleware(request: HttpRequest) -> HttpResponse:
            with settings.__DISHKA_CONTAINER__(
                {HttpRequest: request},
                scope=Scope.SESSION,
            ) as request_container:
                request.META["dishka_container"] = request_container
                return get_response(request)

    return (
        async_middleware
        if iscoroutinefunction(get_response)
        else sync_middleware
    )
