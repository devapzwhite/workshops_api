from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.core.security import current_user, require_roles
from app.models.user import User
from app.schemas.workshop import WorkshopCreate, WorkshopUpdate, WorkshopRead
from app.services import workshop_service

router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.get("", response_model=list[WorkshopRead])
async def list_workshops(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Listar todos los talleres"""
    return await workshop_service.get_all_workshops(db)


@router.post("", response_model=WorkshopRead, status_code=status.HTTP_201_CREATED)
async def create_workshop(
    data: WorkshopCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles("ADMIN"))]
):
    """Crear un nuevo taller (solo ADMIN)"""
    return await workshop_service.create_workshop(db, data)


@router.get("/{workshop_id}", response_model=WorkshopRead)
async def get_workshop(
    workshop_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Obtener un taller por ID"""
    return await workshop_service.get_workshop_by_id(db, workshop_id)


@router.put("/{workshop_id}", response_model=WorkshopRead)
async def update_workshop(
    workshop_id: int,
    data: WorkshopUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles("ADMIN"))]
):
    """Actualizar un taller (solo ADMIN)"""
    return await workshop_service.update_workshop(db, workshop_id, data)


@router.delete("/{workshop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workshop(
    workshop_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles("ADMIN"))]
):
    """Eliminar un taller (solo ADMIN)"""
    await workshop_service.delete_workshop(db, workshop_id)
