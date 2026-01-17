"""Authentication routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """
    Register a new user.

    Args:
        user_data: User registration data (email and password)
        db: Database session

    Returns:
        UserRead: Created user information
    """
    auth_service = AuthService(db)
    return await auth_service.register_user(user_data)


@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Login user and get access token.

    Args:
        login_data: User login credentials (email and password)
        db: Database session

    Returns:
        Token: JWT access token
    """
    auth_service = AuthService(db)
    return await auth_service.login_user(login_data)


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user information",
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Get current authenticated user information.

    Args:
        current_user: Current authenticated user from JWT token

    Returns:
        UserRead: Current user information
    """
    return UserRead.model_validate(current_user)

