from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from app.enums import WorkOrderItemType



class WorkOrderItemBase(BaseModel):
    work_order_id: int = Field(..., alias="Work Order ID")
    item_type: WorkOrderItemType = Field(..., alias="Work Order Type")
    description: str = Field(..., alias="Description")
    quantity: int = Field(default=1, ge=1, alias="Quantity")
    unit_cost: Decimal = Field(default=Decimal(0) ,ge=0, alias="Unit Cost")
    unit_price: Decimal = Field(default=Decimal(0),ge=0, alias="Unit Price")
    before_photo: Optional[str] | None = Field(None, alias="Before Photo")
    after_photo: Optional[str] | None = Field(None, alias="After Photo")

class WorkOrderItemCreate(WorkOrderItemBase):
    work_order_id: int

class WorkOrderItemUpdate(BaseModel):
    item_type:        Optional[WorkOrderItemType] = None
    description:      Optional[str]               = Field(default=None, min_length=1)
    quantity:         Optional[int]               = Field(default=None, ge=1)
    unit_cost:        Optional[Decimal]           = Field(default=None, ge=0)
    unit_price:       Optional[Decimal]           = Field(default=None, ge=0)
    before_photo_url: Optional[str]               = None
    after_photo_url:  Optional[str]               = None

class WorkOrderItemResponse(WorkOrderItemBase):
    id:            int
    work_order_id: int
    model_config = ConfigDict(from_attributes=True)