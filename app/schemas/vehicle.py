from datetime import datetime

from app.enums import TipoVehiculo
from pydantic import BaseModel, Field


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