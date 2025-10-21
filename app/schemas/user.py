"""
Pydantic schemas for user api requests and responses
"""

import uuid
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

from app.models import UserStatus
# Base Schemas


class UserBase(BaseModel):
    """Base user schema with common fields"""

    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(BaseModel):
    """Schema for user registration"""

    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "adityag",
                "email": "adityagurram06@example.com",
                "password": "Aditya7874",
                "display_name": "Aditya Gurram",
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema for updating user profile"""

    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    status: Optional[UserStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "display_name": "Aditya Gurram",
                "avatar_url": "https://example.com/avatar.jpg",
                "status": "online",
            }
        }
    )


class UserLogin(BaseModel):
    """Schema for user login"""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={"example": {"username": "adityag", "password": "Aditya8988"}}
    )


# Response Schemas
class UserResponse(BaseModel):
    """Schema for user data in API responses"""

    id: uuid.UUID
    username: str
    email: EmailStr
    display_name: str
    avatar_url: Optional[str] = None
    status: UserStatus
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "adityag",
                "email": "adityagurram06@example.com",
                "display_name": "Aditya Gurram",
                "avatar_url": "https://example.com/avatar.jpg",
                "status": "online",
                "last_seen": "2025-10-20T12:00:00Z",
                "created_at": "2025-10-01T08:00:00Z",
                "updated_at": "2025-10-20T12:00:00Z",
            }
        },
    )


class UserPublicResponse(BaseModel):
    """Schema for public user data (limited info for other users)"""

    id: uuid.UUID
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    status: UserStatus
    last_seen: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "adityag",
                "display_name": "Aditya Gurram",
                "avatar_url": "https://example.com/avatar.jpg",
                "status": "online",
                "last_seen": "2025-10-20T12:00:00Z",
            }
        }
    )


#  Authentication Schemas


class Token(BaseModel):
    """Schema for JWT token response"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    )


class TokenData(BaseModel):
    """Schema for decoded token data"""

    user_id: Optional[uuid.UUID] = None


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""

    refresh_token: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        }
    )
