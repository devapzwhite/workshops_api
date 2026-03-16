from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.workshop import Workshop
from app.schemas.workshop import WorkshopCreate, WorkshopUpdate


async def get_all_workshops(db: AsyncSession) -> list[Workshop]:
    """Obtener todos los talleres"""
    result = await db.execute(select(Workshop).order_by(Workshop.name))
    return list(result.scalars().all())


async def get_workshop_by_id(db: AsyncSession, workshop_id: int) -> Workshop:
    """Obtener un taller por ID"""
    result = await db.execute(select(Workshop).where(Workshop.id == workshop_id))
    workshop = result.scalars().first()
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Taller con id {workshop_id} no encontrado"
        )
    return workshop


async def create_workshop(db: AsyncSession, workshop_data: WorkshopCreate) -> Workshop:
    """Crear un nuevo taller"""
    new_workshop = Workshop(
        name=workshop_data.name,
        owner_name=workshop_data.owner_name,
        phone=workshop_data.phone,
        address=workshop_data.address
    )
    db.add(new_workshop)
    await db.commit()
    await db.refresh(new_workshop)
    return new_workshop


async def update_workshop(db: AsyncSession, workshop_id: int, workshop_data: WorkshopUpdate) -> Workshop:
    """Actualizar un taller"""
    workshop = await get_workshop_by_id(db, workshop_id)
    
    update_data = workshop_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workshop, key, value)
    
    await db.commit()
    await db.refresh(workshop)
    return workshop


async def delete_workshop(db: AsyncSession, workshop_id: int) -> None:
    """Eliminar un taller"""
    workshop = await get_workshop_by_id(db, workshop_id)
    await db.delete(workshop)
    await db.commit()
