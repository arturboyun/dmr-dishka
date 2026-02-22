import pytest
from dishka import (
    Provider,
    Scope,
    make_async_container,
    provide,
)

from dmr_dishka.integration import setup_dishka


class TestProvider(Provider):
    @provide(scope=Scope.SESSION)
    def provide_str(self) -> str:
        return "Hello from Dishka!"


@pytest.fixture(scope="session", autouse=True)
def setup_test_container() -> None:
    """
    Set up a test container with a single provider that returns a string.  This container is used in both the middleware and integration tests to verify that
    the same dependencies are resolved throughout the
    """
    container = make_async_container(TestProvider())
    setup_dishka(container)
