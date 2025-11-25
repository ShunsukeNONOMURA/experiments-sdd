from __future__ import annotations

from math import ceil
from typing import Any

from pydantic import BaseModel, Field

from app.core.config import settings


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=settings.pagination_default_limit, ge=1, le=settings.pagination_max_limit)

    def offset(self) -> int:
        return (self.page - 1) * self.limit

    def clamp(self) -> "PaginationParams":
        limit = min(self.limit, settings.pagination_max_limit)
        return PaginationParams(page=self.page, limit=limit)


class PaginationMeta(BaseModel):
    totalCount: int
    page: int
    pageSize: int
    hasNext: bool

    @classmethod
    def from_counts(cls, total: int, params: PaginationParams) -> "PaginationMeta":
        total_pages = max(ceil(total / params.limit), 1)
        has_next = params.page < total_pages
        return cls(totalCount=total, page=params.page, pageSize=params.limit, hasNext=has_next)


def apply_pagination(query, params: PaginationParams) -> Any:
    clamped = params.clamp()
    return query.offset(clamped.offset()).limit(clamped.limit)
