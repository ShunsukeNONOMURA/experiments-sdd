from __future__ import annotations

from typing import Iterable, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User, UserRole, UserStatus
from app.schemas.users import StatusFilter


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_users(self, *, page: int, limit: int, status: StatusFilter | UserStatus | str) -> Tuple[list[User], int]:
        base_stmt = select(User)
        if status != StatusFilter.all:
            desired = UserStatus(status) if isinstance(status, str) else status
            base_stmt = base_stmt.where(User.status == desired)
        total_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = self.session.scalar(total_stmt) or 0
        query = base_stmt.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit)
        items = self.session.execute(query).scalars().all()
        return items, total

    def get_by_email(self, email: str) -> User | None:
        normalized = email.lower().strip()
        stmt = select(User).where(User.email == normalized)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_id(self, user_id: str) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def create_user(self, *, name: str, email: str, role: UserRole) -> User:
        user = User(name=name.strip(), email=email.lower().strip(), role=role, status=UserStatus.active)
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user

    def soft_delete_user(self, user_id: str) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        if user.status == UserStatus.inactive:
            return user
        user.status = UserStatus.inactive
        self.session.add(user)
        return user
