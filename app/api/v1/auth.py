import jwt
from fastapi import APIRouter, Depends, HTTPException,status

from app.core.security import authenticate_user,generate_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db

router = APIRouter(prefix="/auth",tags=["auth"])


@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = authenticate_user(db=db,username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Inactive user")
    data_to_encode = {"username": user.username,
                      "name": user.full_name,
                      "shop_id": user.shop_id}
    return generate_token(data_to_encode)

# RESULTADO
# {
#     "data": {
#         "username": "yonaxv",
#         "name": "hoover apaza",
#         "exp": "2026-02-11T05:19:29.568981+00:00"
#     },
#     "token": {
#         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InlvbmF4diIsIm5hbWUiOiJob292ZXIgYXBhemEiLCJzaG9wX2lkIjoxLCJleHAiOjE3NzA3ODcxNjl9.aF2yTURlacR6UQPvumTXzyE3TvdMLwV0ACDvCSjDDzQ",
#         "token_type": "bearer"
#     }
# }