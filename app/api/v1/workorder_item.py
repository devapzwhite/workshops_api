from typing import Annotated, List, Optional
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.security import current_user
from app.schemas.work_order_item import WorkOrderItemCreate, WorkOrderItemUpdate, WorkOrderItemResponse
from app.models.user import User
from app.models.work_order_item import WorkOrderItem
from app.models.work_order import WorkOrder
from app.db.database import get_db

router = APIRouter(prefix='/workorderitem', tags=['Work Order Item'])


@router.get('/', response_model=List[WorkOrderItemResponse])
async def get_workorder_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)],
    work_order_id: Optional[int] = Query(None, alias="workOrderId"),
):
    if work_order_id:
        # Verificar que la orden pertenece al taller del usuario
        wo_result = await db.execute(
            select(WorkOrder).where(
                WorkOrder.id == work_order_id,
                WorkOrder.shop_id == current_user.shop_id
            )
        )
        work_order = wo_result.scalars().first()
        if not work_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work order not found")

        result = await db.execute(
            select(WorkOrderItem).where(WorkOrderItem.work_order_id == work_order_id)
        )
        return list(result.scalars())

    # Retornar todos los items del taller del usuario via join
    result = await db.execute(
        select(WorkOrderItem)
        .join(WorkOrder, WorkOrderItem.work_order_id == WorkOrder.id)
        .where(WorkOrder.shop_id == current_user.shop_id)
    )
    return list(result.scalars())


@router.get('/{id}', response_model=WorkOrderItemResponse)
async def get_workorder_item_by_id(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)],
):
    result = await db.execute(
        select(WorkOrderItem)
        .join(WorkOrder, WorkOrderItem.work_order_id == WorkOrder.id)
        .where(
            WorkOrderItem.id == id,
            WorkOrder.shop_id == current_user.shop_id
        )
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work order item not found")
    return item


@router.post('/', response_model=WorkOrderItemResponse, status_code=status.HTTP_201_CREATED)
async def create_workorder_item(
    payload: WorkOrderItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)],
):
    # Verificar que la orden de trabajo pertenece al taller del usuario
    print(payload.work_order_id)
    wo_result = await db.execute(
        select(WorkOrder).where(
            WorkOrder.id == payload.work_order_id,
            WorkOrder.shop_id == current_user.shop_id
        )
    )
    work_order = wo_result.scalars().first()
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work order not found")

    new_item = WorkOrderItem(
        work_order_id=payload.work_order_id,
        item_type=payload.item_type,
        description=payload.description,
        quantity=payload.quantity,
        unit_cost=payload.unit_cost,
        unit_price=payload.unit_price,
        before_photo_url=payload.before_photo,
        after_photo_url=payload.after_photo,
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@router.put('/{id}', response_model=WorkOrderItemResponse)
async def update_workorder_item(
    id: int,
    payload: WorkOrderItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)],
):
    result = await db.execute(
        select(WorkOrderItem)
        .join(WorkOrder, WorkOrderItem.work_order_id == WorkOrder.id)
        .where(
            WorkOrderItem.id == id,
            WorkOrder.shop_id == current_user.shop_id
        )
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work order item not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_workorder_item(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)],
):
    result = await db.execute(
        select(WorkOrderItem)
        .join(WorkOrder, WorkOrderItem.work_order_id == WorkOrder.id)
        .where(
            WorkOrderItem.id == id,
            WorkOrder.shop_id == current_user.shop_id
        )
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work order item not found")

    await db.delete(item)
    await db.commit()
