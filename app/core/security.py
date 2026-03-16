from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from pydantic import BaseModel
from app.core.config import Settings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.user import User
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.dependencies import get_db




settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class token(BaseModel):
    access_token: str
    token_type: str



password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password,hashed_password)

async def authenticate_user(db, username,password) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def generate_token(data: dict,)-> dict:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = token(access_token=jwt.encode(to_encode,settings.SECRET_KEY,
        algorithm=settings.ALGORITHM),
        token_type="bearer")
    return {"access_token": encoded_jwt.access_token, "token_type": encoded_jwt.token_type,"exp": expire,"user":data}

async def current_user(token: Annotated[str,Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)])-> User:
    try:
        user_data = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        username = user_data["username"]
        shop_id = user_data["shop_id"]
        response = await db.execute(select(User).where(User.username == username, User.shop_id == shop_id))
        user: User = response.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario Inexistente")
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

def current_user_is_active(user: Annotated[User,Depends(current_user)]) -> User | HTTPException:
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario inactivo")


def require_roles(*allowed_roles: str):
    """
    Dependencia para verificar que el usuario tiene uno de los roles permitidos.
    
    Uso:
        @router.get("/admin-only")
        def endpoint_admin(user: User = Depends(require_roles("ADMIN"))):
            ...
    """
    async def role_checker(
        user: Annotated[User, Depends(current_user_is_active)],
        db: AsyncSession = Depends(get_db)
    ) -> User:
        # Cargar roles del usuario desde la DB
        result = await db.execute(
            select(User)
            .where(User.id == user.id)
        )
        db_user = result.scalars().first()
        
        if not db_user or not db_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes"
            )
        
        user_role_names = [role.name for role in db_user.roles]
        
        # Verificar si el usuario tiene al menos uno de los roles permitidos
        if not any(role in user_role_names for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los roles: {', '.join(allowed_roles)}"
            )
        
        return db_user
    
    return role_checker
