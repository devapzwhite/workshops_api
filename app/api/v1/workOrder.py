from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated, List, Optional
from fastapi import APIRouter, status, HTTPException, Depends, Query

from app.core.security import current_user
from app.schemas.work_order import WorkOrdersRead, NewWorkOrder, WorkOrderUpdate
from app.models.user import User
from app.db.database import get_db
from app.models import WorkOrder
from app.services.workorder_service import new_work_order, get_all_workorders, get_workorder_by_id,update_work_order_by_id

router = APIRouter(prefix="/workorders", tags=["Work Orders"])


@router.get("/", response_model=List[WorkOrdersRead] | WorkOrdersRead)
async def get_workorders(db: Annotated[AsyncSession,
Depends(get_db)],current_user :Annotated[User, Depends(current_user) ],
workOrderId: Optional[int] = Query(None,alias="id"),
) :
    if workOrderId:
        return  await get_workorder_by_id(db=db,id=workOrderId,workshop_id=current_user.shop_id)
    return await get_all_workorders(db=db,workshop_id=current_user.shop_id)

@router.post("/", response_model=WorkOrdersRead)
async def create_workorder(
        work_order: NewWorkOrder,
        db: Annotated[AsyncSession,Depends(get_db)],
current_user :Annotated[User, Depends(current_user) ]
):
    return  await new_work_order(db=db,current_user=current_user,work_order=work_order)

@router.put("/{id}", response_model=WorkOrdersRead)
async def update_work_order(
        id: int,
        payload: WorkOrderUpdate,
        db: Annotated[AsyncSession,Depends(get_db)],
        current_user :Annotated[User, Depends(current_user) ]
):
    return await update_work_order_by_id(db=db,current_user=current_user,id=id,payload=payload)