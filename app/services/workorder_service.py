from typing import Annotated, List
from fastapi import Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import WorkOrder, User
from app.models.work_order_item import WorkOrderItem
from app.schemas.work_order import NewWorkOrder,WorkOrderUpdate,WorkOrdersReadId
from app.services.vehicle_service import get_vehicle_by_id


async def new_work_order(db: AsyncSession,work_order:NewWorkOrder,current_user: User)->WorkOrdersReadId:
    vehicle = await get_vehicle_by_id(id=work_order.vehicle_id, db=db, workshop_id=current_user.shop_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    create_order = WorkOrder(
        vehicle_id=work_order.vehicle_id,
        shop_id=current_user.shop_id,
        created_by_user_id= current_user.id,
        initial_diagnosis=work_order.initial_diagnosis,
        labor_estimate=work_order.labor_estimate,
        parts_estimate=work_order.parts_estimate,
        status=work_order.status,
        notes=work_order.notes,
    )
    try:
        db.add(create_order)
        await db.flush()
        if work_order.workorder_items is not None:
            for item in work_order.workorder_items:
                create_item = WorkOrderItem(
                    work_order_id= create_order.id,
                    item_type= item.item_type,
                    quantity= item.quantity,
                    unit_price= item.unit_price,
                    description= item.description,
                )
                db.add(create_item)
        await db.commit()
        await db.refresh(create_order)
        result = await get_workorder_by_id(db=db,id=create_order.id,workshop_id=current_user.shop_id)
        return result
    except:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def get_all_workorders(db: AsyncSession,
                             workshop_id: int)->List[WorkOrder]:
    result = await db.execute(
        select(WorkOrder).where(WorkOrder.shop_id == workshop_id))
    return list(result.scalars())



async def get_workorder_by_id(db: AsyncSession,
                             workshop_id: int,
                              id: int)->WorkOrdersReadId:
    result = await db.execute(select(WorkOrder).where(WorkOrder.shop_id == workshop_id, WorkOrder.id == id).options(selectinload(WorkOrder.workorder_items)))
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
