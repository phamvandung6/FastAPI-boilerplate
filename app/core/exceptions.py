"""Custom exceptions and exception handlers."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle validation errors.

    Args:
        request: FastAPI request
        exc: Validation exception

    Returns:
        JSONResponse: Error response
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """
    Handle database integrity errors.

    Args:
        request: FastAPI request
        exc: Integrity error

    Returns:
        JSONResponse: Error response
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Database integrity error. This record may already exist."},
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle application exceptions.

    Args:
        request: FastAPI request
        exc: Application exception

    Returns:
        JSONResponse: Error response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
