from __future__ import annotations

from fastapi import APIRouter, Depends, Query, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.observability import get_trace_id
from app.db.session import get_db
from app.schemas.users import StatusFilter, UserCreate, UserCreatedResponse, UserListResponse
from app.services.errors import DuplicateEmailError, UserNotFoundError
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", summary="List users", response_model=UserListResponse)
async def list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    status: StatusFilter = Query(default=StatusFilter.active),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    result = service.list_users(page=page, limit=limit, status=status)
    result.traceId = get_trace_id()
    return result


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft delete user",
)
async def delete_user(user_id: str, db: Session = Depends(get_db)) -> Response:
    service = UserService(db)
    try:
        service.soft_delete_user(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": exc.code, "message": "User not found", "traceId": get_trace_id()},
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    response_model=UserCreatedResponse,
)
async def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        result = service.create_user(name=payload.name, email=payload.email, role=payload.role)
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": exc.code, "message": "Email already exists", "traceId": get_trace_id()},
        ) from exc
    result.traceId = get_trace_id()
    return result
