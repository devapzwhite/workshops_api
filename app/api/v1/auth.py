from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException,status

from app.core.security import authenticate_user,generate_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db

router = APIRouter(prefix="/auth",tags=["auth"])


@router.post("")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Annotated[AsyncSession,Depends(get_db)]):

    user = await authenticate_user(db=db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Inactive user")
    data_to_encode = {"id": user.id, "username": user.username, "email": user.email,
                      "name": user.full_name,
                      "shop_id": user.shop_id}
    return generate_token(data_to_encode)