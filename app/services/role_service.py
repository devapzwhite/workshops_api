from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.role import Role, UserRole
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate


async def get_all_roles(db: AsyncSession) -> list[Role]:
    """Obtener todos los roles"""
    result = await db.execute(select(Role).order_by(Role.name))
    return list(result.scalars().all())


async def get_role_by_id(db: AsyncSession, role_id: int) -> Role:
    """Obtener un rol por ID"""
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalars().first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con id {role_id} no encontrado"
        )
    return role


async def get_role_by_name(db: AsyncSession, name: str) -> Role | None:
    """Obtener un rol por nombre"""
    result = await db.execute(select(Role).where(Role.name == name))
    return result.scalars().first()


async def create_role(db: AsyncSession, role_data: RoleCreate) -> Role:
    """Crear un nuevo rol"""
    existing = await get_role_by_name(db, role_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El rol '{role_data.name}' ya existe"
        )
    
    new_role = Role(name=role_data.name, description=role_data.description)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role


async def update_role(db: AsyncSession, role_id: int, role_data: RoleUpdate) -> Role:
    """Actualizar un rol"""
    role = await get_role_by_id(db, role_id)
    
    if role_data.name is not None:
        existing = await get_role_by_name(db, role_data.name)
        if existing and existing.id != role_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El rol '{role_data.name}' ya existe"
            )
        role.name = role_data.name
    
    if role_data.description is not None:
        role.description = role_data.description
    
    await db.commit()
    await db.refresh(role)
    return role


async def delete_role(db: AsyncSession, role_id: int) -> None:
    """Eliminar un rol"""
    role = await get_role_by_id(db, role_id)
    await db.delete(role)
    await db.commit()


async def assign_role_to_user(db: AsyncSession, user_id: int, role_id: int) -> UserRole:
    """Asignar un rol a un usuario"""
    # Verificar que existe el usuario
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado"
        )
    
    # Verificar que existe el rol
    role = await get_role_by_id(db, role_id)
    
    # Verificar que el usuario no tiene ya ese rol
    result = await db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya tiene este rol asignado"
        )
    
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)
    return user_role


async def remove_role_from_user(db: AsyncSession, user_id: int, role_id: int) -> None:
    """Quitar un rol de un usuario"""
    result = await db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    )
    user_role = result.scalars().first()
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene este rol asignado"
        )
    
    await db.delete(user_role)
    await db.commit()


async def get_user_roles(db: AsyncSession, user_id: int) -> list[Role]:
    """Obtener todos los roles de un usuario"""
    result = await db.execute(
        select(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    return list(result.scalars().all())
