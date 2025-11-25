from __future__ import annotations

import pytest

from app.models.user import User, UserRole, UserStatus


@pytest.mark.asyncio
async def test_create_user_success(client):
    payload = {"name": "Alice", "email": "alice@example.com", "role": "admin"}
    response = await client.post("/users", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "alice@example.com"
    assert body["user"]["status"] == "active"
    assert "traceId" in body


@pytest.mark.asyncio
async def test_create_user_duplicate_email_returns_conflict(client, db_session):
    user = User(name="Bob", email="bob@example.com", role=UserRole.viewer, status=UserStatus.active)
    db_session.add(user)
    db_session.commit()

    payload = {"name": "Bob", "email": "bob@example.com", "role": "viewer"}
    response = await client.post("/users", json=payload)

    assert response.status_code == 409
    assert response.json()["code"] == "USER_DUPLICATE_EMAIL"
