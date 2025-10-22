"""
User service for business logic and database operations
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.models.user import UserStatus


class UserService:
    """Service class for user operatins."""

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Create a new user.
        Args:
            db: database session
            user_data: User registration data
        Returns:
            Created user object
        Raises:
            ValueError: if username or email address already exists
        """
        existing_user = UserService.get_by_username(db, user_data.username)
        if existing_user:
            raise ValueError("Username already registered.")

        # check if email exists
        existing_email = UserService.get_by_email(db, user_data.email)
        if existing_email:
            raise ValueError("Email already registered.")
        hashed_password = get_password_hash(user_data.password)

        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            display_name=user_data.display_name,
            status=UserStatus.OFFLINE,
        )
        db.add(db_user)

        try:
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError:
            await db.rollback()
            raise ValueError("Username or email already registered.")

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user with username and password.

        Args:
            db:Database session
            username: username
            password: Plain password
        Returns:
            User object if authentication successful, None otherwise
        """
        user = UserService.get_by_username(db, username)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    async def update_user(db: AsyncSession, user: User, user_data: UserUpdate) -> User:
        """
        Update user profile.

        Args:
            db: Database session
            user: User object to update
            user_data: Update data

        Returns:
            Updated user object
        """
        update_data = user_data.model_dump(exclude_unset=True)
        update_data = {
            field: value for field, value in update_data.items() if value is not None
        }

        for field, value in update_data.items():
            setattr(user, field, value)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def update_status(db: AsyncSession, user: User, status: UserStatus) -> User:
        from datetime import datetime, timezone

        user.status = status
        if status == UserStatus.OFFLINE:
            user.last_seen = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(user)

        return user
