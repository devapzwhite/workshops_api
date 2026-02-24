from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.enums import statusWorkOrder


class WorkOrder(BaseModel):
    vehicle_id: int = Field(...)
    initial_diagnosis: str | None = Field(None)
    labor_estimate: Decimal | None = Field(None,ge=0,decimal_places=2)
    parts_estimate: Decimal | None = Field(None, ge=0,decimal_places=2)
    status: statusWorkOrder
    notes: str | None = Field(None)

class NewWorkOrder(WorkOrder):
    pass

class WorkOrdersRead(WorkOrder):
    id: int
    shop_id: int
    created_by_user_id: int
    check_in_at: datetime
    check_out_at: datetime | None
    created_at: datetime | None
    class Config:
        from_attributes= True


class WorkOrdersUpdate(BaseModel):
    check_out_at: datetime | None = None
    labor_estimate: Decimal | None = Field(None,ge=0,decimal_places=2)
    parts_estimate: Decimal | None = Field(None,ge=0,decimal_places=2)
    status : statusWorkOrder | None= None



# CREATE TABLE work_orders (
#     id                   SERIAL PRIMARY KEY,
#     shop_id              INTEGER NOT NULL REFERENCES workshops(id) ON DELETE CASCADE,
#     vehicle_id           INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
#     created_by_user_id   INTEGER REFERENCES users(id),
#     check_in_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     check_out_at         TIMESTAMP,
#     initial_diagnosis    TEXT,
#     labor_estimate       NUMERIC(12,2) default 0,
#     parts_estimate       NUMERIC(12,2) default 0,
#     status               VARCHAR(30) NOT NULL
#         CHECK (status IN (
#             'RECEIVED',
#             'DIAGNOSIS',
#             'WAITING_APPROVAL',
#             'APPROVED',
#             'IN_PROGRESS',
#             'WAITING_PARTS',
#             'REPAIRED',
#             'READY_FOR_DELIVERY',
#             'COMPLETED',
#             'CANCELLED'
#         )),
#     notes                TEXT,
#     created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );