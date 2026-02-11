import os

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from pydantic import BaseModel
from app.models.user import User
from datetime import datetime, timezone, timedelta

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class token(BaseModel):
    access_token: str
    token_type: str
class tokenData(BaseModel):
    username: str


password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def authenticate_user(db, username,password) -> User | None:
    print(username,password)
    user = db.query(User).filter(User.username == username).first()
    print(user)
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
    return {"access_token": encoded_jwt.access_token, "token_type": encoded_jwt.token_type,"user":data}