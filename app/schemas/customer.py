from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

from app.schemas.vehicle import VehicleRead
from app.schemas.workshop import WorkshopBase


class CustomerBase(BaseModel):
    document_id: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=200)

class CustomerCreate(CustomerBase):
    pass


# ---- Para actualizar (opcional) ----
class CustomerUpdate(BaseModel):
    document_id: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=200)

# ---- Para responder (lectura) ----
class CustomerRead(CustomerBase):
    id: int
    shop_id: int
    created_at: datetime
    vehicles: Optional[List[VehicleRead]]

    class Config:
        from_attributes = True


class CustomerReadDetail(CustomerBase):
    id: int
    workshop: WorkshopBase
    created_at: datetime
    vehicles: Optional[List[VehicleRead]]

    class Config:
        from_attributes = True