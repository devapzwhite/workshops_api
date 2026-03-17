from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from app.enums import StatusWorkOrder, WorkOrderItemType
from app.schemas.work_order_item import WorkOrderItemResponse


# Campo Decimal reutilizable
def money_field(default=None):
    return Field(default, ge=0, max_digits=12, decimal_places=2)


class WorkOrderItemNested(BaseModel):
    """Schema para items dentro de NewWorkOrder (con URLs opcionales)."""
    item_type: WorkOrderItemType = Field(...)
    description: str = Field(...)
    quantity: int = Field(default=1, ge=1)
    unit_cost: Decimal = Field(default=Decimal(0), ge=0)
    unit_price: Decimal = Field(default=Decimal(0), ge=0)
    before_photo_url: Optional[str] = None
    after_photo_url: Optional[str] = None


class WorkOrderBase(BaseModel):
    initial_diagnosis: str | None = Field(None)
    labor_estimate: Decimal | None = money_field()
    parts_estimate: Decimal | None = money_field()
    status: StatusWorkOrder
    notes: str | None = Field(None)

class NewWorkOrder(WorkOrderBase):
    vehicle_id: int = Field(...)
    workorder_items: List[WorkOrderItemNested] | None = Field(None)

class WorkOrdersRead(WorkOrderBase):
    id: int
    shop_id: int
    vehicle_id: int
    created_by_user_id: Optional[int] = None
    check_in_at: datetime
    check_out_at: datetime | None
    created_at: datetime | None
    model_config = ConfigDict(from_attributes=True)

class WorkOrdersReadId(WorkOrderBase):
    id: int
    vehicle_id: Optional[int] = None
    shop_id: int
    created_by_user_id: Optional[int] = None
    check_in_at: datetime
    check_out_at: datetime | None
    created_at: datetime | None
    workorder_items: Optional[List[WorkOrderItemResponse]]
    model_config = ConfigDict(from_attributes=True)



class WorkOrderUpdate(BaseModel):
    check_out_at:   Optional[datetime]       = None
    labor_estimate: Optional[Decimal]        = money_field()
    parts_estimate: Optional[Decimal]        = money_field()
    status:         Optional[StatusWorkOrder] = None
    notes:          Optional[str]            = None
    initial_diagnosis: Optional[str]         = None
