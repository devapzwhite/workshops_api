import os
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy import select  # ← esta línea debe estar
from sqlalchemy.ext.asyncio import AsyncSession  # ← y esta también


from app.models.user import User
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.dependencies import get_db
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class token(BaseModel):
    access_token: str
    token_type: str
class tokenData(BaseModel):
    username: str


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
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = token(access_token=jwt.encode(to_encode,SECRET_KEY,
        algorithm=ALGORITHM),
        token_type="bearer")
    return {"access_token": encoded_jwt.access_token, "token_type": encoded_jwt.token_type,"exp": expire,"user":data}

async def current_user(token: Annotated[str,Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)])-> None | User | HTTPException:
    try:
        user_data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
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
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario inactivo")
