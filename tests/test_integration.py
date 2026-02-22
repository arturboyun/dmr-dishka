"""
Integration tests for the inject decorator via the full Django
request/response cycle.

The session-scoped `setup_test_container` fixture in conftest.py registers
the test container with setup_dishka so that container_middleware and
inject both resolve dependencies from the same TestProvider.
"""

import json

import pytest
from django.test import AsyncClient


@pytest.mark.django_db(transaction=True)
async def test_user_list_returns_200() -> None:
    """GET /api/users/ should succeed."""
    response = await AsyncClient().get("/api/users/")
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
async def test_user_list_returns_list() -> None:
    """Response body should be a JSON array."""
    response = await AsyncClient().get("/api/users/")
    data = json.loads(response.content)
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.django_db(transaction=True)
async def test_user_list_inject_resolves_str_dependency() -> None:
    """
    inject should pull the str dependency from the dishka container
    and pass it into UserListBlueprint.get.  The view puts the resolved
    value in meta['from_dishka'], so we can assert on the response body.
    """
    response = await AsyncClient().get("/api/users/")
    data = json.loads(response.content)
    assert data[0]["meta"]["from_dishka"] == "Hello from Dishka!"
