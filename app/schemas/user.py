"""
Pydantic schemas for user api requests and responses
"""

from pydantic import BaseModel, Field

# Base Schemas


class UserBase(BaseModel):
    """Base user schema with common fields"""

    username: str = Field(..., min_length=3, max_length=50, pattern="^")
