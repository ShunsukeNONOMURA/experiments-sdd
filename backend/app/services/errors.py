from __future__ import annotations


class ServiceError(Exception):
    code: str = "SERVICE_ERROR"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.code)


class DuplicateEmailError(ServiceError):
    code = "USER_DUPLICATE_EMAIL"


class UserNotFoundError(ServiceError):
    code = "USER_NOT_FOUND"
