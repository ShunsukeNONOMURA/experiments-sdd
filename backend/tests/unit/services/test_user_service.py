from __future__ import annotations

import pytest

from app.models.user import User, UserRole, UserStatus
from app.services.errors import DuplicateEmailError, UserNotFoundError
from app.services.user_service import UserService


def test_create_user_normalizes_email(db_session):
    service = UserService(db_session)
    result = service.create_user(name="Alice", email="Alice@Example.com", role=UserRole.admin)

    assert result.email == "alice@example.com"
    assert result.status == UserStatus.active


def test_create_user_raises_on_duplicate_email(db_session):
    db_session.add(User(name="Bob", email="bob@example.com", role=UserRole.viewer, status=UserStatus.active))
    db_session.commit()
    service = UserService(db_session)

    with pytest.raises(DuplicateEmailError):
        service.create_user(name="Other", email="bob@example.com", role=UserRole.viewer)


def test_soft_delete_user_marks_inactive(db_session):
    user = User(name="Carl", email="carl@example.com", role=UserRole.editor, status=UserStatus.active)
    db_session.add(user)
    db_session.commit()

    service = UserService(db_session)
    result = service.soft_delete_user(user.user_id)

    assert result.status == UserStatus.inactive


def test_soft_delete_user_missing_raises(db_session):
    service = UserService(db_session)
    with pytest.raises(UserNotFoundError):
        service.soft_delete_user("missing")
