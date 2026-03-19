from enum import Enum
from typing import Optional, Dict, Any
from fastapi import HTTPException


class ErrorCode(Enum):

    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"

    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    FORBIDDEN_TASK_ACCESS = "FORBIDDEN_TASK_ACCESS"

    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "code": error_code.value,
                "message": message,
                "field": field,
                "details": details or {},
            },
        )


class UserNotFoundException(AppException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.USER_NOT_FOUND,
            message=f"Пользователь с id={user_id} не найден",
            details={"user_id": user_id},
        )


class UserAlreadyExistsException(AppException):
    def __init__(self, field: str, value: str):
        super().__init__(
            status_code=409,
            error_code=ErrorCode.USER_ALREADY_EXISTS,
            message=f"Пользователь с {field}='{value}' уже существует",
            field=field,
            details={field: value},
        )


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=401,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            message="Неверный email или пароль",
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Не авторизован"):
        super().__init__(
            status_code=401,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            message=message,
        )


class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__(
            status_code=401,
            error_code=ErrorCode.INVALID_TOKEN,
            message="Невалидный токен",
        )


class TaskNotFoundException(AppException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.TASK_NOT_FOUND,
            message=f"Задача с id={task_id} не найдена",
            details={"task_id": task_id},
        )


class ForbiddenTaskAccessException(AppException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=403,
            error_code=ErrorCode.FORBIDDEN_TASK_ACCESS,
            message=f"Нет доступа к задаче id={task_id}",
            details={"task_id": task_id},
        )
