
from pydantic import BaseModel, Field, EmailStr



# CREATE TABLE users (
#     id            SERIAL PRIMARY KEY,
#     shop_id       INTEGER NOT NULL REFERENCES workshops(id) ON DELETE CASCADE,
#     username      VARCHAR(50)  NOT NULL,
#     email         VARCHAR(100) NOT NULL,
#     password	  VARCHAR(255) NOT NULL,
#     is_active     BOOLEAN NOT NULL DEFAULT TRUE,
#     created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE (shop_id, email),
#     UNIQUE (shop_id, username)
# );



class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., max_length=255)
