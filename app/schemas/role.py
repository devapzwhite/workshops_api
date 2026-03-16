from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleRead(RoleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserRoleAssign(BaseModel):
    role_id: int


class UserRoleResponse(BaseModel):
    role_id: int
    role_name: str
    assigned_at: datetime

    class Config:
        from_attributes = True
