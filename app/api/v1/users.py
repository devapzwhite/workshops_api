from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db
from app.core.security import current_user, require_roles
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead, UserReadWithRoles
from app.schemas.role import RoleRead
from app.services import user_service, role_service

router = APIRouter(prefix="/workshops/{shop_id}/users", tags=["users"])


@router.get("", response_model=list[UserRead])
async def list_users(
    shop_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Listar todos los usuarios de un taller"""
    # Verificar que el usuario tiene acceso al taller
    if current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este taller")
    return await user_service.get_users_by_workshop(db, shop_id)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    shop_id: int,
    data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles("ADMIN"))]
):
    """Crear un nuevo usuario en un taller (solo ADMIN)"""
    if current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este taller")
    return await user_service.create_user(db, data, shop_id)


@router.get("/{user_id}", response_model=UserReadWithRoles)
async def get_user(
    shop_id: int,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Obtener un usuario por ID"""
    if current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este taller")
    
    user = await user_service.get_user_by_id(db, user_id, shop_id)
    
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()
    roles = [role.name for role in db_user.roles] if db_user.roles else []
    
    return UserReadWithRoles(
        id=user.id,
        shop_id=user.shop_id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        roles=roles
    )


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    shop_id: int,
    user_id: int,
    data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles("ADMIN"))]
):
    """Actualizar un usuario (solo ADMIN)"""
    if current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este taller")
    return await user_service.update_user(db, user_id, data, shop_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    shop_id: int,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles("ADMIN"))]
):
    """Eliminar un usuario (solo ADMIN)"""
    if current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este taller")
    await user_service.delete_user(db, user_id, shop_id)


@router.patch("/{user_id}/active", response_model=UserRead)
async def toggle_user_active(
    shop_id: int,
    user_id: int,
    is_active: bool,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles("ADMIN"))]
):
    """Activar o desactivar un usuario (solo ADMIN)"""
    if current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este taller")
    return await user_service.toggle_user_active(db, user_id, shop_id, is_active)


@router.get("/{user_id}/roles", response_model=list[RoleRead])
async def get_user_roles(
    shop_id: int,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)]
):
    """Obtener los roles de un usuario"""
    if current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a este taller")
    await user_service.get_user_by_id(db, user_id, shop_id)
    return await role_service.get_user_roles(db, user_id)
