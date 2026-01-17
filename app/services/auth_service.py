"""Authentication service for business logic."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repo import UserRepository
from app.schemas.user import Token, UserCreate, UserLogin, UserRead
from app.models.user import User


class AuthService:
    """Service for authentication business logic."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize service with database session.

        Args:
            session: Async database session
        """
        self.session = session
        self.user_repo = UserRepository(session)

    async def register_user(self, user_data: UserCreate) -> UserRead:
        """
        Register a new user.

        Args:
            user_data: User registration data

        Returns:
            UserRead: Created user

        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Hash password and create user
        hashed_password = get_password_hash(user_data.password)
        user = await self.user_repo.create(
            email=user_data.email,
            hashed_password=hashed_password,
        )

        return UserRead.model_validate(user)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.

        Args:
            email: User email
            password: Plain password

        Returns:
            Optional[User]: User if authenticated, None otherwise
        """
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        return user

    async def login_user(self, login_data: UserLogin) -> Token:
        """
        Login user and return access token.

        Args:
            login_data: User login credentials

        Returns:
            Token: JWT access token

        Raises:
            HTTPException: If credentials are invalid
        """
        user = await self.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")
