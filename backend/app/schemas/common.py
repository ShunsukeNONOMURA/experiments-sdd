from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class TraceableModel(BaseModel):
    traceId: str = Field(description="Correlates logs and responses")


class ErrorResponse(TraceableModel):
    code: str = Field(description="Machine readable error code")
    message: str = Field(description="Human readable error detail")


class APIResponse(TraceableModel, Generic[T]):
    data: T
    meta: Optional[dict[str, Any]] = None
