from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from pwdlib import PasswordHash

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

password_hash = PasswordHash.recommended()


async def get_users_by_workshop(db: AsyncSession, shop_id: int) -> list[User]:
    """Obtener todos los usuarios de un taller"""
    result = await db.execute(
        select(User).where(User.shop_id == shop_id).order_by(User.full_name)
    )
    return list(result.scalars().all())


async def get_user_by_id(db: AsyncSession, user_id: int, shop_id: int) -> User:
    """Obtener un usuario por ID"""
    result = await db.execute(
        select(User).where(User.id == user_id, User.shop_id == shop_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado"
        )
    return user


async def get_user_by_username(db: AsyncSession, username: str, shop_id: int) -> User | None:
    """Obtener usuario por username"""
    result = await db.execute(
        select(User).where(User.username == username, User.shop_id == shop_id)
    )
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str, shop_id: int) -> User | None:
    """Obtener usuario por email"""
    result = await db.execute(
        select(User).where(User.email == email, User.shop_id == shop_id)
    )
    return result.scalars().first()


async def create_user(db: AsyncSession, user_data: UserCreate, shop_id: int) -> User:
    """Crear un nuevo usuario en un taller"""
    # Verificar unicidad de username
    existing_username = await get_user_by_username(db, user_data.username, shop_id)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El username '{user_data.username}' ya está en uso"
        )
    
    # Verificar unicidad de email
    existing_email = await get_user_by_email(db, user_data.email, shop_id)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El email '{user_data.email}' ya está en uso"
        )
    
    # Hashear password
    hashed_password = password_hash.hash(user_data.password)
    
    new_user = User(
        shop_id=shop_id,
        username=user_data.username,
        full_name=user_data.full_name,
        email=user_data.email,
        password=hashed_password,
        is_active=user_data.is_active if hasattr(user_data, 'is_active') else True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate, shop_id: int) -> User:
    """Actualizar un usuario"""
    user = await get_user_by_id(db, user_id, shop_id)
    
    # Si se actualiza username, verificar unicidad
    if user_data.username is not None and user_data.username != user.username:
        existing = await get_user_by_username(db, user_data.username, shop_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El username '{user_data.username}' ya está en uso"
            )
        user.username = user_data.username
    
    # Si se actualiza email, verificar unicidad
    if user_data.email is not None and user_data.email != user.email:
        existing = await get_user_by_email(db, user_data.email, shop_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El email '{user_data.email}' ya está en uso"
            )
        user.email = user_data.email
    
    # Actualizar otros campos
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    
    if user_data.password is not None:
        user.password = password_hash.hash(user_data.password)
    
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int, shop_id: int) -> None:
    """Eliminar un usuario"""
    user = await get_user_by_id(db, user_id, shop_id)
    await db.delete(user)
    await db.commit()


async def toggle_user_active(db: AsyncSession, user_id: int, shop_id: int, is_active: bool) -> User:
    """Activar o desactivar un usuario"""
    user = await get_user_by_id(db, user_id, shop_id)
    user.is_active = is_active
    await db.commit()
    await db.refresh(user)
    return user
