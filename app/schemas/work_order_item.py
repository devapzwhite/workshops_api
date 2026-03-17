from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from app.enums import WorkOrderItemType



class WorkOrderItemBase(BaseModel):
    """Schema base para crear items - sin fotos."""
    item_type: WorkOrderItemType = Field(...)
    description: str = Field(...)
    quantity: int = Field(default=1, ge=1)
    unit_cost: Decimal = Field(default=Decimal(0), ge=0)
    unit_price: Decimal = Field(default=Decimal(0), ge=0)


class WorkOrderItemCreate(BaseModel):
    """Schema para crear item (vía JSON)."""
    work_order_id: int
    item_type: WorkOrderItemType = Field(...)
    description: str = Field(...)
    quantity: int = Field(default=1, ge=1)
    unit_cost: Decimal = Field(default=Decimal(0), ge=0)
    unit_price: Decimal = Field(default=Decimal(0), ge=0)


class WorkOrderItemUpdate(BaseModel):
    item_type: Optional[WorkOrderItemType] = None
    description: Optional[str] = Field(default=None, min_length=1)
    quantity: Optional[int] = Field(default=None, ge=1)
    unit_cost: Optional[Decimal] = Field(default=None, ge=0)
    unit_price: Optional[Decimal] = Field(default=None, ge=0)
    before_photo_url: Optional[str] = None
    after_photo_url: Optional[str] = None


class WorkOrderItemResponse(BaseModel):
    """Schema de respuesta - incluye URLs de fotos."""
    id: int
    work_order_id: int
    item_type: WorkOrderItemType
    description: str
    quantity: int
    unit_cost: Decimal
    unit_price: Decimal
    before_photo_url: Optional[str] = None
    after_photo_url: Optional[str] = None
    created_at: datetime | None
    model_config = ConfigDict(from_attributes=True)