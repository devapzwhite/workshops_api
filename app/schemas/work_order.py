from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional

from app.enums import StatusWorkOrder
from app.schemas.work_order_item import WorkOrderItemBase,WorkOrderItemResponse


# Campo Decimal reutilizable
def money_field(default=None):
    return Field(default, ge=0, max_digits=12, decimal_places=2)

class WorkOrderBase(BaseModel):
    initial_diagnosis: str | None = Field(None)
    labor_estimate: Decimal | None = money_field()
    parts_estimate: Decimal | None = money_field()
    status: StatusWorkOrder
    notes: str | None = Field(None)

class NewWorkOrder(WorkOrderBase):
    vehicle_id: int = Field(...)
    workorder_items: list[WorkOrderItemBase] | None = Field(None)

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
    workorder_items: Optional[list[WorkOrderItemResponse]]
    model_config = ConfigDict(from_attributes=True)



class WorkOrderUpdate(BaseModel):
    check_out_at:   Optional[datetime]       = None
    labor_estimate: Optional[Decimal]        = money_field()
    parts_estimate: Optional[Decimal]        = money_field()
    status:         Optional[StatusWorkOrder] = None
    notes:          Optional[str]            = None
    initial_diagnosis: Optional[str]         = None
