from __future__ import annotations

import pytest

from app.models.user import User, UserRole, UserStatus


@pytest.mark.asyncio
async def test_list_users_returns_empty_payload(client):
    response = await client.get("/users")
    assert response.status_code == 200
    payload = response.json()
    assert payload["users"] == []
    assert payload["totalCount"] == 0
    assert payload["page"] == 1
    assert payload["pageSize"] > 0
    assert payload["hasNext"] is False
    assert "traceId" in payload


@pytest.mark.asyncio
async def test_list_users_returns_active_users_only(client, db_session):
    active = User(name="Alice", email="alice@example.com", role=UserRole.admin, status=UserStatus.active)
    inactive = User(name="Bob", email="bob@example.com", role=UserRole.viewer, status=UserStatus.inactive)
    db_session.add_all([active, inactive])
    db_session.commit()

    response = await client.get("/users", params={"page": 1, "limit": 10})

    payload = response.json()
    assert response.status_code == 200
    assert payload["totalCount"] == 1
    assert len(payload["users"]) == 1
    assert payload["users"][0]["email"] == "alice@example.com"
    assert payload["hasNext"] is False

    response_with_all = await client.get("/users", params={"status": "all"})
    assert response_with_all.status_code == 200
    assert response_with_all.json()["totalCount"] == 2
