from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db
from app.core.security import current_user
from app.models.user import User
from app.models.role import Role, UserRole
from app.schemas.role import RoleCreate, RoleUpdate, RoleRead, UserRoleAssign, UserRoleResponse
from app.services import role_service

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleRead])
async def list_roles(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Listar todos los roles disponibles"""
    return await role_service.get_all_roles(db)


@router.post("", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(
    data: RoleCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Crear un nuevo rol"""
    return await role_service.create_role(db, data)


@router.get("/{role_id}", response_model=RoleRead)
async def get_role(
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Obtener un rol por ID"""
    return await role_service.get_role_by_id(db, role_id)


@router.put("/{role_id}", response_model=RoleRead)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Actualizar un rol"""
    return await role_service.update_role(db, role_id, data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Eliminar un rol"""
    await role_service.delete_role(db, role_id)


# === Endpoints para gestionar roles de usuarios ===

@router.get("/users/{user_id}/roles", response_model=list[RoleRead])
async def get_user_roles(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Obtener los roles de un usuario"""
    return await role_service.get_user_roles(db, user_id)


@router.post("/users/{user_id}/roles", status_code=status.HTTP_201_CREATED)
async def assign_role_to_user(
    user_id: int,
    data: UserRoleAssign,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Asignar un rol a un usuario"""
    user_role = await role_service.assign_role_to_user(db, user_id, data.role_id)
    
    # Obtener el nombre del rol para la respuesta
    role = await role_service.get_role_by_id(db, data.role_id)
    return UserRoleResponse(
        role_id=user_role.role_id,
        role_name=role.name,
        assigned_at=user_role.assigned_at
    )


@router.delete("/users/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Quitar un rol de un usuario"""
    await role_service.remove_role_from_user(db, user_id, role_id)
