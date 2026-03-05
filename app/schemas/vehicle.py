from datetime import datetime
from typing import Optional, List
from app.enums import TipoVehiculo, StatusWorkOrder
from pydantic import BaseModel, Field, ConfigDict,EmailStr


class VehicleBase(BaseModel):
    customer_id: int = Field(...)
    vehicle_type: TipoVehiculo
    plate: str = Field(...,max_length=20)
    brand: str = Field(...,max_length=100)
    model: str = Field(...,max_length=100)
    year: int | None = None
    photo_url: str | None = None


class CreateVehicle(VehicleBase):
    pass

class VehicleRead(VehicleBase):
    id: int
    shop_id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class VehicleUpdate(BaseModel):
    customer_id: int | None = None
    vehicle_type: TipoVehiculo | None = None
    plate: str | None = Field(None, max_length=20)
    brand: str | None = Field(None, max_length=100)
    model: str | None = Field(None, max_length=100)
    year: int | None = None
    photo_url: str | None = None

class VehicleCustomerRead(BaseModel):
    id: int
    shop_id: int
    created_at: datetime
    document_id: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=200)


class VehicleWorkOrdersRead(BaseModel):
    id: int
    status: StatusWorkOrder
    vehicle_id: Optional[int] = None
    notes: str | None = None
    shop_id: int
    initial_diagnosis: str | None = None
    created_by_user_id: Optional[int] = None
    check_in_at: datetime
    check_out_at: datetime | None
    created_at: datetime | None
    model_config = ConfigDict(from_attributes=True)


class VehicleDetailRead(VehicleBase):
    id: int
    shop_id: int
    customer_id: int
    created_at: datetime
    customer: VehicleCustomerRead | None
    work_orders: Optional[List[VehicleWorkOrdersRead]]
    model_config = ConfigDict(from_attributes=True)