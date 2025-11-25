from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole, UserStatus


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    role: UserRole


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    userId: str = Field(alias="user_id")
    name: str
    email: EmailStr
    role: UserRole
    status: UserStatus
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")


class UserListResponse(BaseModel):
    users: List[UserRead]
    totalCount: int
    page: int
    pageSize: int
    hasNext: bool
    traceId: str = Field(default="")


class UserCreatedResponse(BaseModel):
    user: UserRead
    traceId: str = Field(default="")


class StatusFilter(str, Enum):
    active = "active"
    inactive = "inactive"
    all = "all"
