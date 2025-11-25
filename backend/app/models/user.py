from __future__ import annotations

import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, String, UniqueConstraint, func, Index

from app.db.session import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("ix_users_status", "status"),
    )

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False)
    email = Column(String(320), nullable=False)
    role = Column(Enum(UserRole, name="user_role"), nullable=False)
    status = Column(Enum(UserStatus, name="user_status"), nullable=False, default=UserStatus.active)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
