
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., max_length=255)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    password: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    id: int
    shop_id: int
    username: str
    full_name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserReadWithRoles(UserRead):
    roles: list[str] = []

    class Config:
        from_attributes = True
