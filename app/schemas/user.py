
from pydantic import BaseModel, Field, EmailStr




class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., max_length=255)
