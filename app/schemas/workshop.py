from symtable import Class
from typing import Optional

from pydantic import BaseModel, Field
from datetime import  datetime


class WorkshopBase(BaseModel):
    name: str = Field(..., max_length=100)
    owner_name: str = Field(..., max_length=100)
    phone: str = Field(..., max_length=20)
    address: str = Field(..., max_length=200)


class WorkshopCreate(WorkshopBase):
    pass


class WorkshopUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    owner_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)

class WorkshopRead(WorkshopBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True




# CREATE TABLE workshops (
#     id          SERIAL PRIMARY KEY,
#     name        VARCHAR(100) NOT NULL,
#     owner_name  VARCHAR(100),
#     phone       VARCHAR(20),
#     address     VARCHAR(200),
#     created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );