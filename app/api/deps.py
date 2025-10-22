"""
API depenedencies for authentication and database sessions.

"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.db.database import get_db
from app.core.security import decode_token

# OAuth2 schema for JWT token
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)], db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from jwt token
    Raises:
        HTTPException: If token is invalid or user not found
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # verify token type
    token_type: str = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user


async def get_current_active_user(
    current_user: Annotated[User, get_current_user],
) -> User:
    """
    Get current active user (can add additional checks here).
    Future: Check if user is banned, suspended, etc.
    """
    # Add additional check here if needed
    # if current_user is banned:
    #   raise HTTPException(status_Code=400, detail= "User is banned.")
    return current_user
