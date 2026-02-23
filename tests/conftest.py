import pytest
from dishka import (
    Provider,
    Scope,
    make_async_container,
    provide,
)

from dmr_dishka.integration import setup_dishka
from dmr_dishka.provider import DjangoProvider


class TestProvider(Provider):
    @provide(scope=Scope.SESSION)
    def provide_str(self) -> str:
        return "Hello from Dishka!"


@pytest.fixture(scope="session", autouse=True)
def setup_test_container() -> None:
    """
    This fixture sets up the Dishka container for testing.
    It is automatically used in all tests.
    """
    container = make_async_container(DjangoProvider(), TestProvider())
    setup_dishka(container)
