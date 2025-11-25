from __future__ import annotations

import pytest

from app.models.user import User, UserRole, UserStatus


@pytest.mark.asyncio
async def test_delete_user_marks_inactive(client, db_session):
    user = User(name="Zoe", email="zoe@example.com", role=UserRole.viewer, status=UserStatus.active)
    db_session.add(user)
    db_session.commit()

    response = await client.delete(f"/users/{user.user_id}")
    assert response.status_code == 204

    db_session.refresh(user)
    assert user.status == UserStatus.inactive


@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    response = await client.delete("/users/non-existent")
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == "USER_NOT_FOUND"
