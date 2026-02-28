from typing import Annotated, List
from fastapi import Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import WorkOrder, User
from app.schemas.work_order import NewWorkOrder,WorkOrderUpdate
from app.services.vehicle_service import get_vehicle_by_id


async def new_work_order(db: AsyncSession,work_order:NewWorkOrder,current_user: User)->WorkOrder:
    vehicle = await get_vehicle_by_id(id=work_order.vehicle_id, db=db, workshop_id=current_user.shop_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    create_order = WorkOrder(
        vehicle_id=work_order.vehicle_id,
        shop_id=current_user.shop_id,
        initial_diagnosis=work_order.initial_diagnosis,
        labor_estimate=work_order.labor_estimate,
        parts_estimate=work_order.parts_estimate,
        status=work_order.status,
        notes=work_order.notes,
    )
    db.add(create_order)
    await db.commit()
    await db.refresh(create_order)
    return create_order

async def get_all_workorders(db: AsyncSession,
                             workshop_id: int)->List[WorkOrder]:
    result = await db.execute(
        select(WorkOrder).where(WorkOrder.shop_id == workshop_id))
    return list(result.scalars())



async def get_workorder_by_id(db: AsyncSession,
                             workshop_id: int,
                              id: int)->WorkOrder:
    result = await db.execute(select(WorkOrder).where(WorkOrder.shop_id == workshop_id, WorkOrder.id == id))
    workorder = result.scalars().first()
    return workorder


async def update_work_order_by_id(db: AsyncSession, id: int, payload: WorkOrderUpdate,current_user: User)->WorkOrder:
    result = await db.execute(select(WorkOrder).where(WorkOrder.shop_id == current_user.shop_id, WorkOrder.id == id))
    workorder = result.scalars().first()
    if not workorder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workorder, key, value)

    await db.commit()
    await db.refresh(workorder)
    return workorder
