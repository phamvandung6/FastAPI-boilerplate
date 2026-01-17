"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.api.v1.routes import auth
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    integrity_error_handler,
    validation_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.

    Args:
        app: FastAPI application instance
    """
    # Startup
    # Here you can add startup logic like creating database tables
    # For production, use Alembic migrations instead
    yield
    # Shutdown
    # Here you can add cleanup logic


# Create FastAPI app
app = FastAPI(
    title="FastAPI Boilerplate",
    description="Production-ready FastAPI boilerplate with authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENVIRONMENT == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(AppException, app_exception_handler)

# Include routers
app.include_router(auth.router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message
    """
    return {
        "message": "Welcome to FastAPI Boilerplate",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "healthy"}
