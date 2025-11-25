from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.pagination import PaginationMeta, PaginationParams
from app.core.audit import record_user_created, record_user_soft_deleted
from app.models.user import UserRole, UserStatus
from app.repositories.user_repository import UserRepository
from app.schemas.users import StatusFilter, UserCreatedResponse, UserListResponse, UserRead
from app.services.errors import DuplicateEmailError, UserNotFoundError


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = UserRepository(session)

    def list_users(self, *, page: int, limit: int, status: str | StatusFilter | UserStatus) -> UserListResponse:
        params = PaginationParams(page=page, limit=limit).clamp()
        items, total = self.repository.list_users(page=params.page, limit=params.limit, status=status)
        meta = PaginationMeta.from_counts(total, params)
        return UserListResponse(
            users=[UserRead.model_validate(item) for item in items],
            totalCount=total,
            page=meta.page,
            pageSize=meta.pageSize,
            hasNext=meta.hasNext,
        )

    def create_user(self, *, name: str, email: str, role: UserRole) -> UserCreatedResponse:
        normalized_email = email.lower().strip()
        if self.repository.get_by_email(normalized_email):
            raise DuplicateEmailError()
        user = self.repository.create_user(name=name, email=normalized_email, role=role)
        self.session.commit()
        record_user_created(user)
        return UserCreatedResponse(user=UserRead.model_validate(user))

    def soft_delete_user(self, user_id: str) -> UserRead:
        user = self.repository.soft_delete_user(user_id)
        if not user:
            raise UserNotFoundError()
        self.session.commit()
        record_user_soft_deleted(user)
        return UserRead.model_validate(user)
