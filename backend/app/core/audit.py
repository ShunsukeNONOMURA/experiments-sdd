from __future__ import annotations

from app.core.observability import log_event
from app.models.user import User


def record_user_created(user: User) -> None:
    log_event("user.created", userId=user.user_id, role=user.role.value, email=user.email)


def record_user_soft_deleted(user: User) -> None:
    log_event("user.soft_deleted", userId=user.user_id, email=user.email)
